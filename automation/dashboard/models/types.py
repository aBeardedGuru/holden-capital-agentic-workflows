from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


@dataclass(frozen=True)
class TriggerRequest:
    file_ids: list[str]
    operator_id: str
    reason: str
    force_retry: bool = False
    dry_run: bool = False

    def payload(self) -> dict[str, Any]:
        canonical = {
            "file_ids": sorted(self.file_ids),
            "operator_id": self.operator_id,
            "reason": self.reason,
            "force_retry": self.force_retry,
            "dry_run": self.dry_run,
        }
        idempotency_key = hashlib.sha256(
            json.dumps(canonical, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()

        return {
            "file_ids": self.file_ids,
            "operator_id": self.operator_id,
            "requested_at": datetime.now(timezone.utc).isoformat(),
            "reason": self.reason,
            "force_retry": self.force_retry,
            "dry_run": self.dry_run,
            "idempotency_key": idempotency_key,
        }


@dataclass
class AuditEvent:
    event_type: str
    operator_id: str
    status: str
    reason: str
    file_ids: list[str] = field(default_factory=list)
    execution_id: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "event_id": uuid4().hex,
            "event_type": self.event_type,
            "operator_id": self.operator_id,
            "file_ids": ",".join(self.file_ids),
            "execution_id": self.execution_id,
            "status": self.status,
            "reason": self.reason,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "metadata": self.metadata,
        }
