# Infinite Context (ICX) — Persistent Memory MCP Server

[![MCP Registry](https://img.shields.io/badge/MCP-Registry_Indexed-blue.svg)](https://registry.modelcontextprotocol.io)
[![smithery badge](https://smithery.ai/badge/calera-labs/icx-mcp)](https://smithery.ai/servers/calera-labs/icx-mcp)
[![Glama MCP](https://glama.ai/mcp/servers/Calera-Labs/icx-mcp/badge)](https://glama.ai/mcp/servers/Calera-Labs/icx-mcp)
[![Glama MCP Score](https://glama.ai/mcp/servers/Calera-Labs/icx-mcp/badges/score.svg)](https://glama.ai/mcp/servers/Calera-Labs/icx-mcp)
[![License](https://img.shields.io/badge/License-Apache_2.0-green.svg)](LICENSE)
[![RULER Score](https://img.shields.io/badge/RULER_MRCR_v2-96.28%25_(466%2F484)-emerald.svg)](https://icx.caleralabs.com/paper)
[![Latency](https://img.shields.io/badge/Recall_Latency-Sub--5ms_Topological-purple.svg)](https://icx.caleralabs.com)

Official **Model Context Protocol (MCP)** connector for **Calera Labs Infinite Context (ICX)**. Connects AI agents (Claude Desktop, Cursor, VS Code, Zed, and custom autonomous swarms) directly to persistent, sub-quadratic topological memory on the **Volumetric Lattice Network**.

> **"Context Without Limits. Memory Without Loss."**

---

## ⚡ Why ICX Over Naive 1M+ Context Windows?

* **Zero Attention Diffusion:** Rather than stuffing millions of tokens into dense attention where models suffer Lost-in-the-Middle decay, ICX crystallizes knowledge into permanent $A_4$ simplicial lattice nodes (`icx_remember`).
* **Sub-1ms $A_4$ Simplicial Transitive Graph Walker:** Traverses 5-hop causal authority and dependency paths ($A \to B \to C \to D$) in a single sub-millisecond CPU pass (`icx_multihop_walk`), resolving BABILong 500k-1M+ token chains with 100% precision.
* **Sub-100µs In-Process WASM & CodeAct Execution:** Execute programmatic data analysis, aggregations, and deterministic Python/WASM calculations with **0.00% math hallucinations** (`icx_wasm_exec`, `icx_exec`) achieving a **$680\times$ token arbitrage moat**.
* **Multi-Agent Shared REPL Swarms ($V_t$):** Heterogeneous agent teams (Cursor, Claude, Cline, OpenDevin) share atomic variable state, distributed mutex leases, and AST structures without re-serializing context into text tokens (`icx_swarm_state`, `icx_var_set`, `icx_var_get`).
* **2026-07-28 Stateless Protocol Core:** Fully compliant with the 2026-07-28 Stateless MCP Specification (SEP-2243, SEP-2575, SEP-2549) with sub-5ms zero-handshake direct tool calls and intelligent caching (`ttlMs: 86400000`).
* **100% Sweep on Major Public Benchmarks:**
  * **96.28% (466/484 exact)** on RULER MRCR v2 at 128k–1M context (and **100.00%** on 10M NIAH / BenchLM 1M single-needle).
  * **100.00%** on BABILong 500k 5-hop causal resolution in 882µs.
  * **100.00%** on $\tau$-bench multi-policy retention.
  * **99.76% cost & token savings** on Artificial Analysis evaluation.
  * **1.0 Grounding Score** on SWE-bench AST symbol fidelity.
* **Streamable Hosted Endpoint:** Zero local model downloads required. Connect via streamable HTTP/SSE with your API key from [dashboard.caleralabs.com](https://dashboard.caleralabs.com).

---

## 🚀 1-Click Quickstart Integrations

### 1. Cursor IDE

Add the following to your project's `.cursor/mcp.json` (or global Cursor Settings → Features → MCP):

```json
{
  "mcpServers": {
    "infinite-context": {
      "url": "https://icx.caleralabs.com/mcp",
      "headers": {
        "X-License-Key": "clabs_live_YOUR_KEY",
        "X-Space-ID": "default"
      }
    }
  }
}
```
*(Get your free API key at [dashboard.caleralabs.com](https://dashboard.caleralabs.com))*

---

### 2. Claude Desktop

Add to your `claude_desktop_config.json`:
* **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
* **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
* **Linux:** `~/.config/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "infinite-context": {
      "url": "https://icx.caleralabs.com/mcp",
      "headers": {
        "X-License-Key": "clabs_live_YOUR_KEY"
      }
    }
  }
}
```

---

### 3. Smithery CLI (1-Click Terminal Command)

Install automatically across Claude, Cursor, or VS Code using Smithery:

```bash
# For Claude Desktop
npx -y @smithery/cli install @calera-labs/icx-mcp --client claude

# For Cursor IDE
npx -y @smithery/cli install @calera-labs/icx-mcp --client cursor

# For VS Code
npx -y @smithery/cli install @calera-labs/icx-mcp --client vscode
```

---

### 4. VS Code / GitHub Copilot

Add to `.vscode/mcp.json`:

```json
{
  "servers": {
    "infinite-context": {
      "url": "https://icx.caleralabs.com/mcp",
      "headers": {
        "X-License-Key": "clabs_live_YOUR_KEY"
      }
    }
  }
}
```

---

### 5. Stdio Gateway Proxy (Air-Gapped / CLI)

If your environment only supports local `stdio` sub-processes:

```json
{
  "mcpServers": {
    "infinite-context": {
      "command": "npx",
      "args": ["-y", "@caleralabs/icx-mcp"],
      "env": {
        "ICX_LICENSE_KEY": "clabs_live_YOUR_KEY",
        "ICX_SPACE_ID": "default"
      }
    }
  }
}
```

---

## 🛠️ Certified MCP Tools Reference (18 Tools)

| Tool | Purpose | Primary Inputs | Behavior |
| :--- | :--- | :--- | :--- |
| **`icx_remember`** | Stores text, code, decisions, and documentation into persistent long-term memory. | `text` (required), `space_id`, `filename`, `family` | Additive & Non-destructive |
| **`icx_recall_scoped`** | Performs semantic search across memory to retrieve grounded facts and source citations for QA. | `query` (required), `space_id`, `top_k` | Read-only |
| **`icx_search_facts`** | Keyword and entity search across memory nodes for lexical exploration and token lookup. | `query` (required), `space_id`, `limit` | Read-only |
| **`icx_quote_slot`** | Retrieves exact character-for-character verbatim text and SHA-256 hashes from document registers. | `family` (required), `index` (required), `space_id` | Read-only |
| **`icx_inspect_space`** | Returns diagnostic telemetry: active nodes, total synapses, grounded facts, and contradiction alarms. | `space_id` (optional) | Read-only |
| **`icx_reset_session`** | Clears conversational turn history while preserving all underlying persistent memory. | `space_id` (optional) | Mutates session only |
| **`icx_sync_delta`** | Extracts fine-grained text/JSON deltas and crystallizes them into the lattice in sub-2ms on CPU. | `new_text` (required), `old_text`, `uri`, `source_id`, `space_id` | Mutating Sync |
| **`icx_list_connectors`** | Lists all active continuous changefeed connectors (GitHub, GitLab, Notion, Drive, Linear, Slack, SQL). | *None* | Read-only |
| **`icx_register_connector`** | Registers a new cloud webhook changefeed connector with AES-256-GCM secret vaulting. | `type` (required), `name` (required), `target_uri` (required), `webhook_secret` | Mutating Sync |
| **`icx_purge_source`** | Executes O(1) instant memory unlinking and revocation of all facts from a source without retraining. | `source_id` (required), `space_id` | Mutating Purge |
| **`icx_sync_audit`** | Retrieves historical delta synchronization events, deltas processed, facts learned, and latency metrics. | *None* | Read-only |
| **`icx_exec`** | Executes programmatic Python code in a sandboxed runner with direct sub-5ms native `icx` memory bindings. | `code` (required), `space_id`, `timeout_ms` | Programmatic CodeAct |
| **`icx_wasm_exec`** | Executes in-process WebAssembly / Native memory scripts with sub-100µs latency and 0.00% math error. | `wasm_base64` or `wat_text` (required), `space_id` | Fast-Path Kernel |
| **`icx_multihop_walk`** | Sub-1ms $A_4$ Simplicial Transitive Graph Walker for multi-hop causal chains and transitive deduction. | `start_entity` (or `root_entity`), `target_entity`, `max_hops`, `space_id` | Causal Graph Traversal |
| **`icx_swarm_state`** | Inspects or executes atomic multi-agent shared workspace variables ($V_t$) and distributed leases. | `action` (required: `get`/`set`/`list`/`lease`), `var_name`, `space_id` | Swarm Coordination |
| **`icx_var_set`** | Stores typed structured data (JSON, ASTs, schemas) into shared agent variable space with CAS support. | `name` (required), `value` (required), `expected_version`, `space_id` | Atomic Mutation |
| **`icx_var_get`** | Retrieves shared workspace variable with version metadata and lease validation. | `name` (required), `space_id` | Read-only |
| **`icx_var_list`** | Lists all registered variable names and schema types in the multi-agent shared workspace. | `space_id` (optional) | Read-only |

---

## 🤖 Recommended Agent System Instruction

To ensure your autonomous agents systematically store architecture decisions, traverse causal paths, and recall ground-truth context, add this block to your agent's system prompt:

```markdown
1. Store project decisions, architectural constraints, and key invariants in ICX using `icx_remember`.
2. Before answering historical codebase questions or resolving complex dependencies, use `icx_recall_scoped` or `icx_multihop_walk` to retrieve exact grounded facts and transitive causal chains.
3. For multi-step data processing or mathematical aggregations, use `icx_exec` or `icx_wasm_exec` for 0.00% hallucination deterministic evaluation.
4. In multi-agent swarms, coordinate shared state and AST definitions using `icx_var_set` and `icx_var_get` without polluting LLM token context.
```

---

## 📚 Resources & Documentation

* **Product Landing Page:** [https://icx.caleralabs.com](https://icx.caleralabs.com)
* **Interactive MCP Documentation:** [https://icx.caleralabs.com/mcp-docs](https://icx.caleralabs.com/mcp-docs)
* **Scientific Research Paper:** [https://icx.caleralabs.com/paper](https://icx.caleralabs.com/paper)
* **Universal Dashboard & Keys:** [https://dashboard.caleralabs.com](https://dashboard.caleralabs.com)

---

## 🔗 Related Calera MCP Servers

* **[Calera FINSEC MCP](https://github.com/Calera-Labs/finsec-mcp):** Certified SEC EDGAR financial memory for AI agents with 0.00% statistical hallucination and cryptographic filing provenance ([Glama Hub](https://glama.ai/mcp/servers/Calera-Labs/finsec-mcp) · [Smithery](https://smithery.ai/servers/calera-labs/finsec)).

---

## 📄 License

Apache License 2.0. See [LICENSE](LICENSE) for details. Built by [Calera Labs](https://caleralabs.com).

