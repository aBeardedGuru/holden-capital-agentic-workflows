from __future__ import annotations

from typing import Any

import requests


class N8nClient:
    def __init__(
        self,
        base_url: str,
        api_key: str,
        trigger_endpoint: str,
        timeout_seconds: int = 30,
        tls_verify: bool = True,
        ca_bundle: str | None = None,
    ):
        self.base_url = base_url.rstrip("/")
        self.trigger_endpoint = trigger_endpoint
        self.timeout_seconds = timeout_seconds
        self.session = requests.Session()
        self.session.verify = ca_bundle if ca_bundle else tls_verify
        self.session.headers.update({
            "X-N8N-API-KEY": api_key,
            "Content-Type": "application/json",
        })

    def _trigger_url(self) -> str:
        if self.trigger_endpoint.startswith("http"):
            return self.trigger_endpoint
        return f"{self.base_url}/{self.trigger_endpoint.lstrip('/')}"

    def trigger(self, payload: dict[str, Any]) -> dict[str, Any]:
        response = self.session.post(self._trigger_url(), json=payload, timeout=self.timeout_seconds)
        response.raise_for_status()
        return _safe_json(response)

    def list_executions(self, limit: int = 20, status: str | None = None) -> list[dict[str, Any]]:
        params: dict[str, Any] = {"limit": limit}
        if status:
            params["status"] = status
        response = self.session.get(f"{self.base_url}/api/v1/executions", params=params, timeout=self.timeout_seconds)
        response.raise_for_status()
        data = _safe_json(response)
        if isinstance(data, dict):
            if "data" in data and isinstance(data["data"], list):
                return data["data"]
            if "results" in data and isinstance(data["results"], list):
                return data["results"]
        if isinstance(data, list):
            return data
        return []

    def get_execution(self, execution_id: str) -> dict[str, Any]:
        response = self.session.get(f"{self.base_url}/api/v1/executions/{execution_id}", timeout=self.timeout_seconds)
        response.raise_for_status()
        data = _safe_json(response)
        return data if isinstance(data, dict) else {"raw": data}

    def stop_execution(self, execution_id: str) -> dict[str, Any]:
        stop_url = f"{self.base_url}/api/v1/executions/{execution_id}/stop"
        response = self.session.post(stop_url, timeout=self.timeout_seconds)
        if response.status_code == 404:
            delete_url = f"{self.base_url}/api/v1/executions/{execution_id}"
            response = self.session.delete(delete_url, timeout=self.timeout_seconds)
        response.raise_for_status()
        data = _safe_json(response)
        return data if isinstance(data, dict) else {"raw": data}


def _safe_json(response: requests.Response) -> Any:
    try:
        return response.json()
    except ValueError:
        return {"text": response.text}
