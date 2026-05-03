from __future__ import annotations

from clients.sheets_client import SheetsClient
from models.types import AuditEvent
from runtime.audit_logger import append_jsonl


class AuditService:
    def __init__(self, sheets: SheetsClient, audit_sheet_name: str, jsonl_path: str):
        self.sheets = sheets
        self.audit_sheet_name = audit_sheet_name
        self.jsonl_path = jsonl_path

    def record(self, event: AuditEvent) -> dict:
        data = event.to_dict()
        append_jsonl(self.jsonl_path, data)
        try:
            self.sheets.append_dict_row(self.audit_sheet_name, data)
        except Exception:
            # Local JSONL is the durability fallback when sheet append fails.
            pass
        return data
