from __future__ import annotations

from google.oauth2 import service_account

SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/spreadsheets",
]


def build_credentials(service_account_file: str):
    return service_account.Credentials.from_service_account_file(
        service_account_file,
        scopes=SCOPES,
    )
