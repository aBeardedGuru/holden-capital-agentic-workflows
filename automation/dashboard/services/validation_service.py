from __future__ import annotations


def validate_upload_constraints(file_name: str, payload: bytes, max_upload_mb: int) -> None:
    if not file_name.strip():
        raise ValueError("Uploaded file has no name")
    max_bytes = max_upload_mb * 1024 * 1024
    if len(payload) > max_bytes:
        raise ValueError(f"File {file_name} exceeds max size ({max_upload_mb}MB)")


def validate_batch_size(file_ids: list[str], max_batch_files: int) -> None:
    if not file_ids:
        raise ValueError("No files selected")
    if len(file_ids) > max_batch_files:
        raise ValueError(f"Batch size exceeds limit ({max_batch_files})")
