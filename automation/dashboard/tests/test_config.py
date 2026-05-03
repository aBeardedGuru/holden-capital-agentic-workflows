from config import REQUIRED_ENV


def test_required_env_declared():
    assert "N8N_BASE_URL" in REQUIRED_ENV
    assert "GOOGLE_SHEETS_LEDGER_ID" in REQUIRED_ENV
