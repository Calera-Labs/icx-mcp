# Calera Agent Memory (`calera-agent-memory`)

> The plug-and-play **AI Memory Substrate** for Python agent swarms, LangChain, and CrewAI.  
> Eliminates LLM context rot with sub-5ms $O(1)$ topological associative memory.

---

## ⚡ Quickstart: 3 Lines of Code

```python
from calera_agent_memory import CaleraMemorySubstrate

# Auto-provisions a free 1,000,000-node persistent vault under Delaware UETA § 14
memory = CaleraMemorySubstrate(principal_email="developer@company.com")

# Drop directly into your agent or LLM chain
memory.save_context({"input": "Project Alpha deadline"}, {"output": "October 15, 2026"})
context = memory.load_memory_variables({"input": "When is the project due?"})
print(context["history"])
```

---

## Direct Client Usage

```python
from calera_agent_memory import CaleraMemoryClient

client = CaleraMemoryClient(api_key="your_optional_api_key")

# Claim free vault
vault_info = client.claim_free_vault("me@example.com", agent_name="my-researcher")

# Store fact into 4D topological lattice
client.store("NVDA_FY26_Rev", "Estimated at $168B based on datacenter expansion")

# Sub-5ms recall with zero token bloat (standard format)
results = client.query("NVDA revenue projection")
print(results)

# 1D Holographic Ribbon Mode (saves >40% prompt injection tokens)
ribbon = client.query_ribbon("NVDA revenue projection")
print(ribbon["ribbon"])
# Output:
# <nav:ribbon premise="NVDA_FY26_Rev" target="DATACENTER" steps=2 action=2.8400>
# NVDA_FY26_Rev -> DATACENTER_EXPANSION -> REVENUE_PROJECTION
# </nav:ribbon>

# Continuous Geodesic Navigation (stationary-action shortest path)
trajectory = client.geodesic(premise="NVDA_FY26_Rev", target="FREE_CASH_FLOW")
print(trajectory["pathway"])
print(trajectory["ribbon"])
```

---

## Key Advantages
- **Sub-5ms Recall:** $O(1)$ topological graph retrieval instead of slow vector database linear scans.
- **1D Holographic Ribbon:** Stationary-action shortest path serialization reduces prompt memory injection from 2,000+ tokens to an 80-token crystal chain.
- **Zero Hallucination Context:** Retains exact structured relationships without semantic degradation.
- **Free 1M Node Tier:** Agents can self-provision permanent memory vaults at runtime for $0.00.

