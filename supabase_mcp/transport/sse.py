import asyncio
from typing import Any
from fastapi import FastAPI
from starlette.requests import Request
from mcp.server.fastmcp import FastMCP
from mcp.server.sse import SseServerTransport
import uvicorn
from supabase_mcp.logger import logger


class SSETransport:
    """Proper MCP-compatible SSE transport using FastMCP's built-in SSE support"""
    
    def __init__(self, mcp_server: FastMCP, host: str = "0.0.0.0", port: int = 8123):
        self.mcp_server = mcp_server
        self.host = host
        self.port = port
        self.app = FastAPI(title="Supabase MCP Server SSE Transport")
        self.setup_routes()
    
    def setup_routes(self):
        """Setup MCP-compatible SSE routes"""
        
        @self.app.get("/")
        async def root():
            return {
                "message": "Supabase MCP Server SSE Transport",
                "endpoints": {
                    "health": "/health",
                    "sse": "/sse",
                    "messages": "/messages"
                }
            }
        
        @self.app.get("/health")
        async def health_check():
            return {"status": "healthy", "transport": "sse"}
        
        # Create MCP SSE transport
        self.sse_transport = SseServerTransport("/messages")
        
        @self.app.get("/sse")
        async def handle_sse(request: Request):
            """SSE endpoint for MCP protocol"""
            async with self.sse_transport.connect_sse(
                request.scope, request.receive, request._send
            ) as (read_stream, write_stream):
                await self.mcp_server.run(
                    read_stream, write_stream, self.mcp_server.create_initialization_options()
                )
        
        @self.app.post("/messages")
        async def handle_messages(request: Request):
            """HTTP endpoint for MCP messages"""
            return await self.sse_transport.handle_post_message(request)
    
    def run(self):
        """Run the SSE server"""
        logger.info(f"Starting Supabase MCP SSE server on {self.host}:{self.port}")
        uvicorn.run(self.app, host=self.host, port=self.port)
