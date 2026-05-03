from __future__ import annotations

import mimetypes
from typing import Any

from clients.drive_client import DriveClient
from clients.n8n_client import N8nClient
from models.types import TriggerRequest
from services.validation_service import validate_batch_size, validate_upload_constraints


class IntakeService:
    def __init__(self, drive: DriveClient, n8n: N8nClient, max_upload_mb: int, max_batch_files: int):
        self.drive = drive
        self.n8n = n8n
        self.max_upload_mb = max_upload_mb
        self.max_batch_files = max_batch_files

    def upload_files(self, folder_id: str, uploads: list[Any]) -> list[dict[str, Any]]:
        results: list[dict[str, Any]] = []
        for upload in uploads:
            payload = upload.getvalue()
            validate_upload_constraints(upload.name, payload, self.max_upload_mb)
            mime_type = mimetypes.guess_type(upload.name)[0] or "application/octet-stream"
            results.append(
                self.drive.upload_file_to_folder(
                    folder_id=folder_id,
                    filename=upload.name,
                    content=payload,
                    mime_type=mime_type,
                )
            )
        return results

    def trigger(self, request: TriggerRequest) -> dict[str, Any]:
        validate_batch_size(request.file_ids, self.max_batch_files)
        return self.n8n.trigger(request.payload())

    def retry(self, file_ids: list[str], operator_id: str, reason: str) -> dict[str, Any]:
        retry_request = TriggerRequest(
            file_ids=file_ids,
            operator_id=operator_id,
            reason=reason,
            force_retry=True,
        )
        return self.trigger(retry_request)
