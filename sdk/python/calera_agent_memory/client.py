"""Client library for interacting with Calera ICX Epistemic Memory."""

import json
import os
import urllib.request
import urllib.error
from typing import Optional, Dict, Any, List


class CaleraMemoryClient:
    """Client for the Calera ICX 4D Topological Memory Substrate."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        vault_id: Optional[str] = None,
        base_url: str = "https://vln-icx-api.caleralabs.com",
        timeout: float = 10.0,
    ):
        self.api_key = api_key or os.environ.get("CALERA_API_KEY")
        self.vault_id = vault_id or os.environ.get("CALERA_VAULT_ID")
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def _request(self, path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Perform a JSON HTTP POST request with proper authentication."""
        url = f"{self.base_url}{path}"
        data = json.dumps(payload).encode("utf-8")
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "CaleraAgentMemory-Python/0.4.1",
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
            headers["X-License-Key"] = self.api_key

        req = urllib.request.Request(url, data=data, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                body = response.read().decode("utf-8")
                return json.loads(body)
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="replace")
            try:
                err_json = json.loads(err_body)
                return {"status": "ERROR", "code": e.code, "error": err_json.get("error", str(e))}
            except Exception:
                return {"status": "ERROR", "code": e.code, "error": err_body or str(e)}
        except Exception as e:
            return {"status": "ERROR", "error": str(e)}

    def claim_free_vault(self, principal_email: str, agent_name: str = "autonomous-agent") -> Dict[str, Any]:
        """Self-provision a 1,000,000-node persistent memory vault under Delaware UETA § 14."""
        payload = {
            "principalEmail": principal_email,
            "agentName": agent_name,
            "acceptA2bTerms": True,
        }
        result = self._request("/api/v1/agent/provision", payload)
        if result.get("status") in ("PROVISIONED", "SUCCESS") or "vaultId" in result:
            self.vault_id = result.get("vaultId", f"vault_free_{hash(principal_email) & 0xFFFFFF}")
            result["vaultId"] = self.vault_id
        return result

    def store(self, concept: str, association: str, vault_id: Optional[str] = None) -> Dict[str, Any]:
        """Store a fact or task state into the topological memory lattice."""
        v_id = vault_id or self.vault_id or "default_vault"
        payload = {
            "vaultId": v_id,
            "concept": concept,
            "association": association,
        }
        return self._request("/api/v1/memory/store", payload)

    def query(
        self,
        query: str,
        max_depth: int = 3,
        format: str = "standard",
        vault_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Retrieve associative memories from the vault in sub-5ms.

        Args:
            query: Question or concept to recall.
            max_depth: Maximum transitive walk depth (default: 3).
            format: Output format ('standard' for JSON facts, 'ribbon' for 1D holographic transition ribbon).
            vault_id: Optional vault namespace override.
        """
        v_id = vault_id or self.vault_id or "default_vault"
        payload = {
            "vaultId": v_id,
            "query": query,
            "maxDepth": max_depth,
            "format": format,
        }
        return self._request("/api/v1/memory/query", payload)

    def query_ribbon(
        self,
        query: str,
        max_depth: int = 3,
        vault_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Convenience method to retrieve memories formatted as a 1D holographic geodesic ribbon."""
        return self.query(query=query, max_depth=max_depth, format="ribbon", vault_id=vault_id)

    def geodesic(
        self,
        premise: str,
        target: str,
        vault_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Calculate continuous stationary-action shortest path across the simplicial complex.

        Returns 1D holographic ribbon serialization (<nav:ribbon>) connecting premise to target.
        """
        v_id = vault_id or self.vault_id or "default_vault"
        payload = {
            "vaultId": v_id,
            "premise": premise,
            "target": target,
        }
        return self._request("/v1/lattice/geodesic", payload)
