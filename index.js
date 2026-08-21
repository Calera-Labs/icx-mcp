#!/usr/bin/env node
/**
 * Official Calera Infinite Context (ICX) MCP Gateway Client
 * Transparently bridges stdio JSON-RPC 2.0 to Calera Volumetric Lattice Network Cloud endpoint.
 */

import readline from 'readline';

const API_ENDPOINT = process.env.ICX_MCP_URL || 'https://icx.caleralabs.com/mcp';
const LICENSE_KEY = process.env.ICX_LICENSE_KEY || process.env.FINSEC_LICENSE_KEY || process.env.X_LICENSE_KEY || 'clabs_live_pilot_review';
const SPACE_ID = process.env.ICX_SPACE_ID || process.env.X_SPACE_ID || 'default';

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
  terminal: false
});

rl.on('line', async (line) => {
  if (!line.trim()) return;

  try {
    const payload = JSON.parse(line);
    const headers = {
      'Content-Type': 'application/json',
      'X-License-Key': LICENSE_KEY,
      'X-Space-ID': SPACE_ID,
      'MCP-Protocol-Version': '2026-07-28',
      'User-Agent': 'Calera-ICX-MCP-Node/0.4.1'
    };

    if (payload && payload.method) {
      headers['Mcp-Method'] = String(payload.method);
      if (payload.params && payload.params.name) {
        headers['Mcp-Name'] = String(payload.params.name);
      }
    }

    // Forward JSON-RPC request to Calera ICX endpoint
    const response = await fetch(API_ENDPOINT, {
      method: 'POST',
      headers,
      body: JSON.stringify(payload)
    });

    const data = await response.json();
    process.stdout.write(JSON.stringify(data) + '\n');
  } catch (err) {
    const errorResponse = {
      jsonrpc: '2.0',
      id: null,
      error: {
        code: -32603,
        message: 'Internal ICX Gateway Error: ' + (err.message || String(err))
      }
    };
    process.stdout.write(JSON.stringify(errorResponse) + '\n');
  }
});
