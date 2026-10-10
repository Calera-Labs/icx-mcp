"""Client library for interacting with Calera ICX Epistemic Memory."""

import json
import os
import urllib.request
import urllib.error
from typing import Optional, Dict, Any, List


class LatticeAPI:
    """Namespace for 4D topological memory lattice operations."""

    def __init__(self, client: "CaleraMemoryClient"):
        self._client = client

    def recall(
        self,
        query: str,
        max_depth: int = 2,
        space_id: Optional[str] = None,
        target_domain: str = "general",
    ) -> Dict[str, Any]:
        """Perform sub-5ms simplicial lattice recall with mathematical boundary refusal (∂² = 0)."""
        return self._client.query(
            query=query,
            max_depth=max_depth,
            vault_id=space_id,
            target_domain=target_domain,
        )

    def store(
        self,
        concept: str,
        association: str,
        space_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Store structured facts or decisions into the persistent 4D topological lattice."""
        return self._client.store(
            concept=concept,
            association=association,
            vault_id=space_id,
        )

    def walk(
        self,
        start_node: str,
        target_node: Optional[str] = None,
        max_hops: int = 5,
        space_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Simplicial transitive lattice walk over associative concept manifolds."""
        payload = {
            "vaultId": space_id or self._client.vault_id or "default_vault",
            "startNode": start_node,
            "targetNode": target_node,
            "maxHops": max_hops,
        }
        return self._client._request("/api/v1/lattice/walk", payload)


class SpacesAPI:
    """Namespace for isolated memory space lifecycle management."""

    def __init__(self, client: "CaleraMemoryClient"):
        self._client = client

    def create(
        self,
        name: str,
        description: str = "",
    ) -> Dict[str, Any]:
        """Create or bind to an isolated, encrypted memory space."""
        payload = {
            "name": name,
            "space_id": name,
            "description": description,
        }
        res = self._client._request("/v1/memory/spaces", payload)
        if isinstance(res, dict) and "space_id" in res:
            self._client.vault_id = res["space_id"]
        elif isinstance(res, dict) and "id" in res:
            self._client.vault_id = res["id"]
        else:
            self._client.vault_id = name
        return res if isinstance(res, dict) else {"space_id": name, "status": "CREATED"}

    def list(self) -> Dict[str, Any]:
        """List active memory spaces for the authenticated tenant."""
        return self._client._request("/v1/memory/spaces", {})


class CaleraMemoryClient:
    """Client for the Calera ICX 4D Topological Memory Substrate."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        vault_id: Optional[str] = None,
        base_url: str = "https://vln-icx-api.caleralabs.com",
        timeout: float = 10.0,
    ):
        self.api_key = api_key or os.environ.get("CALERA_API_KEY") or os.environ.get("ICX_API_KEY")
        self.vault_id = vault_id or os.environ.get("CALERA_VAULT_ID") or os.environ.get("ICX_SPACE_ID")
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.lattice = LatticeAPI(self)
        self.spaces = SpacesAPI(self)

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
        target_domain: str = "general",
    ) -> Dict[str, Any]:
        """Retrieve associative memories from the vault in sub-5ms.

        Args:
            query: Question or concept to recall.
            max_depth: Maximum transitive walk depth (default: 3).
            format: Output format ('standard' for JSON facts, 'ribbon' for 1D holographic transition ribbon).
            vault_id: Optional vault namespace override.
            target_domain: Subspace domain filter ('general', 'finsec', 'icx').
        """
        v_id = vault_id or self.vault_id or "default_vault"
        payload = {
            "vaultId": v_id,
            "query": query,
            "maxDepth": max_depth,
            "format": format,
            "targetDomain": target_domain,
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


# Canonical alias for streamlined developer ergonomics
CaleraClient = CaleraMemoryClient
