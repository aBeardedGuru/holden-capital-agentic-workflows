from __future__ import annotations

import json
from typing import Any

from googleapiclient.discovery import build


class SheetsClient:
    def __init__(self, credentials, spreadsheet_id: str):
        self.service = build("sheets", "v4", credentials=credentials)
        self.spreadsheet_id = spreadsheet_id

    def append_dict_row(self, sheet_name: str, row: dict[str, Any]) -> None:
        headers = self._get_headers(sheet_name)
        values: list[str] = []
        for header in headers:
            value = row.get(header, "")
            if isinstance(value, (dict, list)):
                values.append(json.dumps(value))
            else:
                values.append(str(value))

        (
            self.service.spreadsheets()
            .values()
            .append(
                spreadsheetId=self.spreadsheet_id,
                range=f"{sheet_name}!A1",
                valueInputOption="USER_ENTERED",
                insertDataOption="INSERT_ROWS",
                body={"values": [values]},
            )
            .execute()
        )

    def read_rows(self, sheet_name: str, max_rows: int = 250) -> list[dict[str, str]]:
        res = (
            self.service.spreadsheets()
            .values()
            .get(spreadsheetId=self.spreadsheet_id, range=f"{sheet_name}!A1:ZZ{max_rows}")
            .execute()
        )
        rows = res.get("values", [])
        if not rows:
            return []

        headers = rows[0]
        mapped: list[dict[str, str]] = []
        for row in rows[1:]:
            mapped.append({headers[idx]: row[idx] if idx < len(row) else "" for idx in range(len(headers))})
        return mapped

    def _get_headers(self, sheet_name: str) -> list[str]:
        res = (
            self.service.spreadsheets()
            .values()
            .get(spreadsheetId=self.spreadsheet_id, range=f"{sheet_name}!A1:ZZ1")
            .execute()
        )
        rows = res.get("values", [])
        if not rows:
            raise ValueError(f"Sheet '{sheet_name}' has no headers")
        return rows[0]
