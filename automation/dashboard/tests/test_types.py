from models.types import TriggerRequest
from models.types import AuditEvent


def test_trigger_payload_shape():
    request = TriggerRequest(file_ids=["f1"], operator_id="op", reason="manual")
    payload = request.payload()
    payload2 = request.payload()
    assert payload["file_ids"] == ["f1"]
    assert payload["operator_id"] == "op"
    assert payload["reason"] == "manual"
    assert "requested_at" in payload
    assert "idempotency_key" in payload
    assert payload["idempotency_key"] == payload2["idempotency_key"]


def test_trigger_idempotency_key_is_order_insensitive():
    left = TriggerRequest(file_ids=["a", "b"], operator_id="op", reason="manual").payload()
    right = TriggerRequest(file_ids=["b", "a"], operator_id="op", reason="manual").payload()
    assert left["idempotency_key"] == right["idempotency_key"]


def test_audit_event_serialization():
    event = AuditEvent(
        event_type="start",
        operator_id="op",
        status="ok",
        reason="manual",
        file_ids=["f1", "f2"],
    )
    data = event.to_dict()
    assert data["event_type"] == "start"
    assert data["operator_id"] == "op"
    assert data["file_ids"] == "f1,f2"
    assert "event_id" in data
