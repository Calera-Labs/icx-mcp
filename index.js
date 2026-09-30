#!/usr/bin/env node
/**
 * Official Calera Infinite Context (ICX) MCP Gateway Client
 * Transparently bridges stdio JSON-RPC 2.0 to Calera Volumetric Lattice Network Cloud endpoint,
 * with unified cross-MCP credentials and automatic space derivation (~/.calera/icx.env).
 *
 * Copyright (c) 2026 Calera Computing Inc.
 * Licensed under the Apache License, Version 2.0.
 */

import readline from 'node:readline';
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import crypto from 'node:crypto';

const CALERA_CONFIG_DIR = path.join(os.homedir(), '.calera');
const CALERA_ENV_FILE = path.join(CALERA_CONFIG_DIR, 'icx.env');

// Dynamically resolves current ICX license key, space ID, and endpoint across:
// 1. Explicit process environment variables (ICX_API_KEY, ICX_LICENSE_KEY, CALERA_API_KEY, etc.)
// 2. Persistent user config ~/.calera/icx.env (written by @caleralabs/llm-vm-mcp claim_free_icx_tokens or dashboard)
// 3. Local workspace ./.env
// 4. Deterministic space derivation (space_<sha256(key)[:12]>)
// 5. Default pilot review fallback
export function resolveICXConfig() {
  let endpoint = process.env.ICX_MCP_URL || null;
  let licenseKey = null;
  let spaceId = process.env.ICX_SPACE_ID || process.env.SPACE_ID || process.env.X_SPACE_ID || null;

  // 1. Process environment variables
  if (process.env.ICX_API_KEY && process.env.ICX_API_KEY.trim()) {
    licenseKey = process.env.ICX_API_KEY.trim();
  } else if (process.env.ICX_LICENSE_KEY && process.env.ICX_LICENSE_KEY.trim()) {
    licenseKey = process.env.ICX_LICENSE_KEY.trim();
  } else if (process.env.CALERA_API_KEY && process.env.CALERA_API_KEY.trim()) {
    licenseKey = process.env.CALERA_API_KEY.trim();
  } else if (process.env.FINSEC_LICENSE_KEY && process.env.FINSEC_LICENSE_KEY.trim()) {
    licenseKey = process.env.FINSEC_LICENSE_KEY.trim();
  } else if (process.env.X_LICENSE_KEY && process.env.X_LICENSE_KEY.trim()) {
    licenseKey = process.env.X_LICENSE_KEY.trim();
  }

  // 2. Check ~/.calera/icx.env (written by @caleralabs/llm-vm-mcp)
  if (fs.existsSync(CALERA_ENV_FILE)) {
    try {
      const content = fs.readFileSync(CALERA_ENV_FILE, 'utf8');
      if (!licenseKey) {
        const keyMatch = content.match(/(?:ICX_API_KEY|ICX_LICENSE_KEY|CALERA_API_KEY)=([^\s#]+)/);
        if (keyMatch && keyMatch[1]) {
          licenseKey = keyMatch[1].trim();
        }
      }
      if (!spaceId) {
        const spaceMatch = content.match(/(?:SPACE_ID|ICX_SPACE_ID|X_SPACE_ID)=([^\s#]+)/);
        if (spaceMatch && spaceMatch[1]) {
          spaceId = spaceMatch[1].trim();
        }
      }
      if (!endpoint) {
        const urlMatch = content.match(/ICX_MCP_URL=([^\s#]+)/);
        if (urlMatch && urlMatch[1]) {
          endpoint = urlMatch[1].trim();
        }
      }
    } catch (e) {}
  }

  // 3. Local workspace .env
  const localEnv = path.join(process.cwd(), '.env');
  if (fs.existsSync(localEnv)) {
    try {
      const content = fs.readFileSync(localEnv, 'utf8');
      if (!licenseKey) {
        const keyMatch = content.match(/(?:ICX_API_KEY|ICX_LICENSE_KEY|CALERA_API_KEY)=([^\s#]+)/);
        if (keyMatch && keyMatch[1]) {
          licenseKey = keyMatch[1].trim();
        }
      }
      if (!spaceId) {
        const spaceMatch = content.match(/(?:SPACE_ID|ICX_SPACE_ID)=([^\s#]+)/);
        if (spaceMatch && spaceMatch[1]) {
          spaceId = spaceMatch[1].trim();
        }
      }
      if (!endpoint) {
        const urlMatch = content.match(/ICX_MCP_URL=([^\s#]+)/);
        if (urlMatch && urlMatch[1]) {
          endpoint = urlMatch[1].trim();
        }
      }
    } catch (e) {}
  }

  // Default endpoint if not specified
  if (!endpoint) {
    endpoint = 'https://icx.caleralabs.com/mcp';
  }

  // Fallback license key
  if (!licenseKey) {
    licenseKey = 'clabs_live_pilot_review';
  }

  // Deterministic space ID derivation matching @caleralabs/llm-vm-mcp
  if (!spaceId) {
    if (licenseKey && licenseKey !== 'clabs_live_pilot_review' && licenseKey !== 'anonymous') {
      spaceId = 'space_' + crypto.createHash('sha256').update(licenseKey).digest('hex').slice(0, 12);
    } else {
      spaceId = 'default';
    }
  }

  return {
    endpoint,
    licenseKey,
    spaceId,
  };
}

import { fileURLToPath } from 'node:url';

const isMain = process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url);

if (isMain) {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
    terminal: false
  });

  rl.on('line', async (line) => {
    if (!line.trim()) return;

    try {
      const payload = JSON.parse(line);
      const config = resolveICXConfig();

      const headers = {
        'Content-Type': 'application/json',
        'X-License-Key': config.licenseKey,
        'X-Space-ID': config.spaceId,
        'MCP-Protocol-Version': '2026-07-28',
        'User-Agent': 'Calera-ICX-MCP-Node/1.4.0'
      };

      if (payload && payload.method) {
        headers['Mcp-Method'] = String(payload.method);
        if (payload.params && payload.params.name) {
          headers['Mcp-Name'] = String(payload.params.name);

          // Grounding guarantee: If space_id is omitted by the agent in tool arguments,
          // automatically inject the unified user space ID.
          if (payload.params.arguments && typeof payload.params.arguments === 'object') {
            if (!payload.params.arguments.space_id && config.spaceId && config.spaceId !== 'default') {
              payload.params.arguments.space_id = config.spaceId;
            }
          }
        }
      }

      // Forward JSON-RPC request to Calera ICX endpoint
      const response = await fetch(config.endpoint, {
        method: 'POST',
        headers,
        body: JSON.stringify(payload),
        signal: AbortSignal.timeout(10000),
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
}
