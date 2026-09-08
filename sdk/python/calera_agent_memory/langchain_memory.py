"""LangChain & CrewAI compatible memory substrate adapter."""

from typing import Dict, Any, List, Optional
from .client import CaleraMemoryClient


class CaleraMemorySubstrate:
    """Turnkey memory adapter compatible with LangChain BaseMemory and CrewAI agents."""

    def __init__(
        self,
        vault_id: Optional[str] = None,
        api_key: Optional[str] = None,
        principal_email: Optional[str] = None,
        memory_key: str = "history",
    ):
        self.memory_key = memory_key
        self.client = CaleraMemoryClient(api_key=api_key, vault_id=vault_id)
        if not vault_id and principal_email:
            # Auto-provision a free 1M node memory vault on initialization!
            self.client.claim_free_vault(principal_email=principal_email, agent_name="langchain-agent")

    @property
    def memory_variables(self) -> List[str]:
        return [self.memory_key]

    def load_memory_variables(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Fetch topological context relevant to the incoming prompt."""
        query_text = ""
        for key in ("input", "question", "query", "user_input"):
            if key in inputs:
                query_text = str(inputs[key])
                break
        if not query_text:
            query_text = str(next(iter(inputs.values()))) if inputs else ""

        res = self.client.query(query=query_text)
        memories = res.get("associations", []) or res.get("results", [])
        if isinstance(memories, list):
            context_str = "\n".join([f"- {m}" for m in memories if isinstance(m, str)])
        else:
            context_str = str(memories)

        return {self.memory_key: context_str}

    def save_context(self, inputs: Dict[str, Any], outputs: Dict[str, Any]) -> None:
        """Persist user inputs and model outputs into the topological lattice."""
        input_text = str(inputs.get("input", next(iter(inputs.values())) if inputs else ""))
        output_text = str(outputs.get("output", next(iter(outputs.values())) if outputs else ""))
        if input_text and output_text:
            self.client.store(concept=input_text[:100], association=output_text)

    def clear(self) -> None:
        """Clear local buffer or reset transient context."""
        pass
