from __future__ import annotations

import io
from typing import Any

from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload


class DriveClient:
    def __init__(self, credentials):
        self.service = build("drive", "v3", credentials=credentials)

    def list_folder_files(self, folder_id: str, page_size: int = 100) -> list[dict[str, Any]]:
        query = f"'{folder_id}' in parents and mimeType != 'application/vnd.google-apps.folder' and trashed = false"
        res = (
            self.service.files()
            .list(
                q=query,
                pageSize=page_size,
                orderBy="createdTime desc",
                fields="files(id,name,mimeType,size,createdTime,modifiedTime,webViewLink)",
            )
            .execute()
        )
        return res.get("files", [])

    def list_multi_folder(self, folder_map: dict[str, str], page_size: int = 50) -> list[dict[str, Any]]:
        rows: list[dict[str, Any]] = []
        for folder_name, folder_id in folder_map.items():
            for row in self.list_folder_files(folder_id, page_size=page_size):
                row["dashboard_folder"] = folder_name
                rows.append(row)
        return sorted(rows, key=lambda item: item.get("createdTime", ""), reverse=True)

    def upload_file_to_folder(self, folder_id: str, filename: str, content: bytes, mime_type: str) -> dict[str, Any]:
        media = MediaIoBaseUpload(io.BytesIO(content), mimetype=mime_type, resumable=False)
        body = {"name": filename, "parents": [folder_id]}
        return (
            self.service.files()
            .create(body=body, media_body=media, fields="id,name,mimeType,size,webViewLink,createdTime")
            .execute()
        )
