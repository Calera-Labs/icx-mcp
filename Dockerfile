FROM node:20-slim

WORKDIR /app

COPY package.json ./
COPY index.js ./

RUN chmod +x index.js

ENV ICX_MCP_URL=https://icx.caleralabs.com/mcp
ENV ICX_LICENSE_KEY=clabs_live_pilot_review
ENV ICX_SPACE_ID=default

ENTRYPOINT ["node", "index.js"]
