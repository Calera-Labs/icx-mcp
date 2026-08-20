# Contributing to Calera Infinite Context (ICX) MCP

Thank you for your interest in contributing to the **Infinite Context MCP Connector**!

## Development Setup

The ICX MCP Gateway is designed to be zero-dependency and lightweight:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Calera-Labs/icx-mcp.git
   cd icx-mcp
   ```

2. **Verify syntax:**
   ```bash
   node --check index.js
   ```

3. **Run local gateway:**
   ```bash
   ICX_LICENSE_KEY=your_key node index.js
   ```

## Pull Request Guidelines

1. **Keep it lightweight:** Do not introduce large runtime dependencies unless strictly necessary for MCP spec compliance.
2. **Schema Invariants:** Any new tools or schema updates must be reflected synchronously across `smithery.yaml`, `server.json`, `glama.json`, and `README.md`.
3. **Commit Messages:** Follow Conventional Commits format (e.g. `feat: ...`, `fix: ...`, `docs: ...`).

## Code of Conduct

Please treat all community members with respect. We adhere to standard open source community guidelines.
