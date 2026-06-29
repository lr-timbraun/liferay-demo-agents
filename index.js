#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const http = require('http');
const https = require('https');

// 1. Helper to read and parse local .env from current working directory (project root)
function getLiferayConfig() {
    const workspacePath = process.env.WORKSPACE_PATH || process.cwd();
    const envPath = path.join(workspacePath, '.env');
    if (!fs.existsSync(envPath)) {
        return null;
    }
    
    const config = {};
    try {
        const content = fs.readFileSync(envPath, 'utf8');
        content.split(/\r?\n/).forEach(line => {
            const trimmed = line.trim();
            if (trimmed && !trimmed.startsWith('#') && trimmed.includes('=')) {
                const [key, ...valParts] = trimmed.split('=');
                const val = valParts.join('=').trim().replace(/^['"]|['"]$/g, '');
                config[key.trim()] = val;
            }
        });
    } catch (e) {
        return null;
    }
    
    return {
        host: config.LIFERAY_HOST || 'https://localhost',
        email: config.LIFERAY_ADMIN_EMAIL_ADDRESS || '',
        password: config.LIFERAY_ADMIN_PASSWORD || ''
    };
}

// 2. Pure Node.js HTTP/HTTPS Client (zero-dependency, supports Basic Auth and Self-Signed Traefik Bypass)
function makeHttpRequest(config, endpointPath, method = 'GET', payload = null) {
    return new Promise((resolve, reject) => {
        if (!config) {
            return reject(new Error("No active local .env configuration found. This project might not be initialized yet. Run '/lda:init' first."));
        }
        
        // Normalize endpoint path to avoid double slashes
        const normalizedPath = '/' + endpointPath.replace(/^\//, '');
        const targetUrlStr = `${config.host}${normalizedPath}`;
        
        let parsedUrl;
        try {
            parsedUrl = new URL(targetUrlStr);
        } catch (e) {
            return reject(new Error(`Invalid target URL: ${targetUrlStr}`));
        }
        
        const isHttps = parsedUrl.protocol === 'https:';
        const client = isHttps ? https : http;
        
        const authHeader = 'Basic ' + Buffer.from(`${config.email}:${config.password}`).toString('base64');
        
        const options = {
            method: method.toUpperCase(),
            hostname: parsedUrl.hostname,
            port: parsedUrl.port || (isHttps ? 443 : 80),
            path: parsedUrl.pathname + parsedUrl.search,
            headers: {
                'Authorization': authHeader,
                'Accept': 'application/json',
                'User-Agent': 'Gemini-CLI-Liferay-Proxy'
            }
        };
        
        let bodyData = null;
        if (payload) {
            bodyData = typeof payload === 'string' ? payload : JSON.stringify(payload);
            options.headers['Content-Type'] = 'application/json';
            options.headers['Content-Length'] = Buffer.byteLength(bodyData);
        }
        
        const req = client.request(options, (res) => {
            let data = '';
            res.on('data', (chunk) => { data += chunk; });
            res.on('end', () => {
                if (res.statusCode >= 200 && res.statusCode < 300) {
                    try {
                        resolve(JSON.parse(data));
                    } catch (e) {
                        resolve({ rawText: data, message: "Response was not JSON" });
                    }
                } else {
                    reject(new Error(`Liferay returned HTTP ${res.statusCode}: ${data}`));
                }
            });
        });
        
        req.on('error', (e) => {
            reject(new Error(`Failed to connect to Liferay at ${config.host}. Ensure LDM containers are running and healthy. Details: ${e.message}`));
        });
        
        if (bodyData) {
            req.write(bodyData);
        }
        req.end();
    });
}

// 3. Stdio Model Context Protocol (MCP) JSON-RPC Server
let buffer = '';

process.stdin.on('data', (chunk) => {
    buffer += chunk.toString();
    let lineEndIndex;
    
    while ((lineEndIndex = buffer.indexOf('\n')) !== -1) {
        const line = buffer.slice(0, lineEndIndex).trim();
        buffer = buffer.slice(lineEndIndex + 1);
        
        if (line) {
            handleRequest(line);
        }
    }
});

function sendResponse(id, result, error = null) {
    const response = { jsonrpc: '2.0', id };
    if (error) {
        response.error = error;
    } else {
        response.result = result;
    }
    process.stdout.write(JSON.stringify(response) + '\n');
}

async function handleRequest(line) {
    let req;
    try {
        req = JSON.parse(line);
    } catch (e) {
        // Parse error
        sendResponse(null, null, { code: -32700, message: "Parse error" });
        return;
    }
    
    const { method, params, id } = req;
    
    if (method === 'initialize') {
        sendResponse(id, {
            protocolVersion: '2024-11-05',
            capabilities: { tools: {} },
            serverInfo: { name: 'liferay-demo-agents-proxy', version: '0.1.1' }
        });
        return;
    }
    
    if (method === 'notifications/initialized') {
        // Initialized notification has no response
        return;
    }
    
    if (method === 'ping') {
        sendResponse(id, {});
        return;
    }
    
    if (method === 'tools/list') {
        sendResponse(id, {
            tools: [
                {
                    name: 'liferay_get_openapis',
                    description: 'Queries Liferay\'s central headless API directory and returns all available services, categories, and their endpoints.',
                    inputSchema: {
                        type: 'object',
                        properties: {},
                        required: []
                    }
                },
                {
                    name: 'liferay_get_openapi',
                    description: 'Fetches the complete OpenAPI JSON schema for a specific Liferay REST service endpoint (e.g. \'/o/headless-delivery/v1.0/openapi.json\'). Useful to discover schemas and properties.',
                    inputSchema: {
                        type: 'object',
                        properties: {
                            endpointPath: {
                                type: 'string',
                                description: 'The exact endpoint OpenAPI path suffix (e.g., \'/o/headless-delivery/v1.0/openapi.json\').'
                            }
                        },
                        required: ['endpointPath']
                    }
                },
                {
                    name: 'liferay_call_http_endpoint',
                    description: 'Executes a standard HTTP request (GET, POST, PUT, DELETE, PATCH) against a specific Liferay REST endpoint with an optional JSON payload. Enables full dynamic control of Liferay resources (like creating/updating pages or schema mappings).',
                    inputSchema: {
                        type: 'object',
                        properties: {
                            endpointPath: {
                                type: 'string',
                                description: 'The target Liferay REST endpoint URL path suffix (e.g., \'/o/headless-delivery/v1.0/sites/{siteId}/site-pages\').'
                            },
                            method: {
                                type: 'string',
                                enum: ['GET', 'POST', 'PUT', 'DELETE', 'PATCH'],
                                description: 'The HTTP method to execute.'
                            },
                            payload: {
                                type: 'object',
                                description: 'An optional JSON object mapping to the request body payload.'
                            }
                        },
                        required: ['endpointPath', 'method']
                    }
                }
            ]
        });
        return;
    }
    
    if (method === 'tools/call') {
        const { name, arguments: args } = params;
        const config = getLiferayConfig();
        
        try {
            if (name === 'liferay_get_openapis') {
                const res = await makeHttpRequest(config, '/o/api', 'GET');
                sendResponse(id, { content: [{ type: 'text', text: JSON.stringify(res, null, 2) }] });
            } 
            else if (name === 'liferay_get_openapi') {
                const { endpointPath } = args;
                const res = await makeHttpRequest(config, endpointPath, 'GET');
                sendResponse(id, { content: [{ type: 'text', text: JSON.stringify(res, null, 2) }] });
            } 
            else if (name === 'liferay_call_http_endpoint') {
                const { endpointPath, method: httpMethod, payload } = args;
                const res = await makeHttpRequest(config, endpointPath, httpMethod, payload);
                sendResponse(id, { content: [{ type: 'text', text: JSON.stringify(res, null, 2) }] });
            } 
            else {
                sendResponse(id, null, { code: -32601, message: `Method not found: ${name}` });
            }
        } catch (err) {
            // Return error response back to LLM gracefully so it can recover/handle it
            sendResponse(id, {
                isError: true,
                content: [{ type: 'text', text: `Error calling Liferay tool: ${err.message}` }]
            });
        }
        return;
    }
    
    // Method not found for any other JSON-RPC requests
    sendResponse(id, null, { code: -32601, message: `Method not found: ${method}` });
}
