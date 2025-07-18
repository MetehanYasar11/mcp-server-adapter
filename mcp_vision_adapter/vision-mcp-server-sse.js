#!/usr/bin/env node
/**
 * MCP Vision Adapter - N8N Compatible SSE Server
 * Based on n8n-mcp-connector structure
 */

// Use modules from local npm installation
let express, McpServer, SSEServerTransport, z;

try {
    express = require('express');
    
    // MCP SDK with relative path and explicit .js extension
    const { McpServer: McpServerClass } = require('./node_modules/@modelcontextprotocol/sdk/dist/cjs/server/mcp.js');
    const { SSEServerTransport: SSEServerTransportClass } = require('./node_modules/@modelcontextprotocol/sdk/dist/cjs/server/sse.js');
    const zod = require('zod');
    
    McpServer = McpServerClass;
    SSEServerTransport = SSEServerTransportClass;
    z = zod.z;
    
    console.log('✅ Using local npm dependencies');
} catch (error) {
    console.error('❌ Failed to load dependencies:', error.message);
    console.error('❌ Stack trace:', error.stack);
    console.error('Please install required packages: npm install express @modelcontextprotocol/sdk zod');
    process.exit(1);
}

const { randomUUID } = require('node:crypto');
const { spawn } = require('node:child_process');
const fs = require('node:fs');
const path = require('node:path');

// Use node-fetch v2 which is compatible with require()
let fetch, FormData;
try {
  fetch = require('node-fetch');
  FormData = require('form-data');
} catch (error) {
  console.warn('⚠️  node-fetch or form-data not available, HTTP requests will be limited');
}

/**
 * Create the MCP Server with Vision tools
 */
const createVisionServer = () => {
  const server = new McpServer({
    name: 'vision_mcp_adapter',
    version: '1.0.0',
  }, { 
    capabilities: { 
      tools: {},
      logging: {}
    } 
  });

  // Tool 1: Object Detection
  server.tool(
    'detect_objects',
    'Detect objects in an image or video using YOLO',
    {
      image_path: z.string().describe('Path to the image or video file'),
      manual_result: z.string().optional().describe('Optional manual result override')
    },
    async ({ image_path, manual_result }) => {
      try {
        console.log('🔍 Detecting objects in:', image_path.substring(0, 50) + '...');
        
        // If manual result is provided, use it
        if (manual_result) {
          return {
            content: [
              {
                type: 'text',
                text: `✅ Manual result: ${manual_result}`
              }
            ]
          };
        }

        // Check if file exists
        if (!fs.existsSync(image_path)) {
          throw new Error(`File not found: ${image_path}`);
        }

        // Call YOLO service with retry mechanism
        const YOLO_SERVICE = process.env.YOLO_SERVICE_URL || 'http://localhost:8080';
        
        if (!fetch || !FormData) {
          throw new Error('HTTP client dependencies not available');
        }
        
        // Retry mechanism for YOLO service connection
        const retryRequest = async (url, options, maxRetries = 3, delay = 2000) => {
          for (let i = 0; i < maxRetries; i++) {
            try {
              const response = await fetch(url, options);
              if (response.ok) {
                return response;
              }
              throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            } catch (error) {
              console.log(`YOLO service attempt ${i + 1}/${maxRetries} failed:`, error.message);
              if (i === maxRetries - 1) throw error;
              await new Promise(resolve => setTimeout(resolve, delay));
            }
          }
        };
        
        // Create form data
        const formData = new FormData();
        formData.append('file', fs.createReadStream(image_path), path.basename(image_path));

        // Send request to YOLO service with retry
        const response = await retryRequest(`${YOLO_SERVICE}/detect`, {
          method: 'POST',
          body: formData,
          headers: formData.getHeaders()
        });

        if (!response.ok) {
          throw new Error(`YOLO service error: ${response.status} ${response.statusText}`);
        }

        const data = await response.json();
        console.log('📊 YOLO response:', JSON.stringify(data, null, 2));

        // Extract classes from results
        const classes = [];
        if (data.results && Array.isArray(data.results)) {
          for (const result of data.results) {
            const className = result.class_ || result.class || '?';
            classes.push(className);
          }
        }

        if (classes.length === 0) {
          return {
            content: [
              {
                type: 'text',
                text: '✅ No objects detected in the image.'
              }
            ]
          };
        }

        const uniqueClasses = [...new Set(classes)].sort();
        return {
          content: [
            {
              type: 'text',
              text: `✅ Objects detected: ${uniqueClasses.join(', ')}`
            }
          ]
        };

      } catch (error) {
        console.error('❌ Object detection error:', error);
        return {
          content: [
            {
              type: 'text',
              text: `❌ Object detection failed: ${error.message}`
            }
          ],
          isError: true
        };
      }
    }
  );

  // Tool 2: YOLO CLI Operations
  server.tool(
    'yolo_cli',
    'Execute Ultralytics YOLO CLI commands',
    {
      args: z.string().describe('Arguments for the YOLO CLI command (e.g., "predict model=yolov8n.pt source=image.jpg")')
    },
    async ({ args }) => {
      try {
        console.log('🐍 Executing YOLO CLI:', args);
        
        return new Promise((resolve, reject) => {
          // Use virtual environment Python
          const command = '/opt/venv/bin/python';
          const commandArgs = ['-m', 'ultralytics', ...args.split(' ')];
          
          const child = spawn(command, commandArgs, {
            stdio: ['pipe', 'pipe', 'pipe']
          });

          let stdout = '';
          let stderr = '';

          child.stdout.on('data', (data) => {
            stdout += data.toString();
          });

          child.stderr.on('data', (data) => {
            stderr += data.toString();
          });

          child.on('close', (code) => {
            if (code !== 0) {
              resolve({
                content: [
                  {
                    type: 'text',
                    text: `❌ YOLO CLI failed (exit code ${code}):\n${stderr || stdout}`
                  }
                ],
                isError: true
              });
            } else {
              resolve({
                content: [
                  {
                    type: 'text',
                    text: `✅ YOLO CLI completed successfully:\n${stdout || 'Command executed successfully'}`
                  }
                ]
              });
            }
          });

          child.on('error', (error) => {
            resolve({
              content: [
                {
                  type: 'text',
                  text: `❌ YOLO CLI execution error: ${error.message}`
                }
              ],
              isError: true
            });
          });
        });

      } catch (error) {
        console.error('❌ YOLO CLI error:', error);
        return {
          content: [
            {
              type: 'text',
              text: `❌ YOLO CLI failed: ${error.message}`
            }
          ],
          isError: true
        };
      }
    }
  );

  return server;
};

// Create Express application
const app = express();
app.use(express.json());

// Store transports by session ID
const transports = {};

console.log('🚀 Starting MCP Vision Adapter Server...');

//=============================================================================
// SSE TRANSPORT - N8N COMPATIBLE
//=============================================================================
app.get('/sse', async (req, res) => {
  console.log('📡 GET /sse - Establishing SSE connection');
  
  try {
    const transport = new SSEServerTransport('/messages', res);
    transports[transport.sessionId] = transport;
    
    res.on("close", () => {
      console.log(`❌ SSE connection closed for session ${transport.sessionId}`);
      delete transports[transport.sessionId];
    });

    const server = createVisionServer();
    await server.connect(transport);
    
    console.log(`✅ SSE transport connected: ${transport.sessionId}`);
  } catch (error) {
    console.error('❌ SSE connection error:', error);
    if (!res.headersSent) {
      res.status(500).send('Internal server error');
    }
  }
});

app.post("/messages", async (req, res) => {
  const sessionId = req.query.sessionId;
  console.log(`📡 POST /messages: ${sessionId}`);
  
  try {
    const transport = transports[sessionId];
    
    if (transport instanceof SSEServerTransport) {
      await transport.handlePostMessage(req, res, req.body);
    } else {
      res.status(400).json({
        jsonrpc: '2.0',
        error: {
          code: -32000,
          message: 'No transport found for sessionId',
        },
        id: null,
      });
    }
  } catch (error) {
    console.error('❌ POST message error:', error);
    if (!res.headersSent) {
      res.status(500).json({
        jsonrpc: '2.0',
        error: {
          code: -32603,
          message: 'Internal server error',
        },
        id: null,
      });
    }
  }
});

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    server: 'vision_mcp_adapter',
    version: '1.0.0',
    activeSessions: Object.keys(transports).length,
    yoloServiceUrl: process.env.YOLO_SERVICE_URL || 'http://localhost:8080',
    timestamp: new Date().toISOString()
  });
});

// Legacy endpoints for backward compatibility
app.get('/manifest', (req, res) => {
  res.json({
    tools: [
      {
        name: 'detect_objects',
        description: 'Detect objects in an image or video using YOLO',
        inputSchema: {
          type: 'object',
          properties: {
            image_path: { type: 'string' },
            manual_result: { type: 'string', description: 'Optional manual result override' }
          },
          required: ['image_path']
        }
      },
      {
        name: 'yolo_cli',
        description: 'Execute Ultralytics YOLO CLI commands',
        inputSchema: {
          type: 'object',
          properties: {
            args: { type: 'string', description: 'YOLO CLI arguments' }
          },
          required: ['args']
        }
      }
    ]
  });
});

// YOLO Service Health Check
async function waitForYoloService(maxRetries = 30, delay = 2000) {
  const YOLO_SERVICE = process.env.YOLO_SERVICE_URL || 'http://localhost:8080';
  
  for (let i = 0; i < maxRetries; i++) {
    try {
      console.log(`🔍 Checking YOLO service health... (${i + 1}/${maxRetries})`);
      const response = await fetch(`${YOLO_SERVICE}/docs`);
      if (response.ok) {
        console.log('✅ YOLO service is ready!');
        return true;
      }
    } catch (error) {
      console.log(`⏳ YOLO service not ready yet, waiting ${delay}ms...`);
    }
    await new Promise(resolve => setTimeout(resolve, delay));
  }
  
  console.warn('⚠️ YOLO service not available, but starting MCP server anyway...');
  return false;
}

// Start server with YOLO health check
const PORT = process.env.PORT || 3000;

async function startServer() {
  // Wait for YOLO service to be ready
  await waitForYoloService();
  
  app.listen(PORT, '0.0.0.0', () => {
    console.log(`
🎯 MCP Vision Adapter Server Running on Port ${PORT}
==================================================

📡 SSE Endpoint: http://localhost:${PORT}/sse
📨 Messages: http://localhost:${PORT}/messages  
❤️ Health: http://localhost:${PORT}/health
📋 Manifest: http://localhost:${PORT}/manifest

✅ N8N MCP Client Compatible
🔗 YOLO Service: ${process.env.YOLO_SERVICE_URL || 'http://localhost:8080'}
==================================================
    `);
  });
}

startServer();

// Graceful shutdown
process.on('SIGINT', async () => {
  console.log('\n🛑 Shutting down...');
  
  for (const sessionId in transports) {
    try {
      await transports[sessionId].close();
      delete transports[sessionId];
    } catch (error) {
      console.error(`Error closing session ${sessionId}:`, error);
    }
  }
  
  console.log('✅ Shutdown complete');
  process.exit(0);
});
