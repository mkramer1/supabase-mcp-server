import argparse
from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

from fastapi import FastAPI
from mcp.server.fastmcp import FastMCP
from sse_starlette.sse import EventSourceResponse
from starlette.requests import Request
from supabase_mcp.core.container import ServicesContainer
from supabase_mcp.core.server_core import ServerCore
from supabase_mcp.logger import logger
from supabase_mcp.settings import settings
from supabase_mcp.tools.registry import ToolRegistry
from supabase_mcp.transport.sse import SSETransport
import uvicorn

def run_server_stdio(core: ServerCore) -> None:
    """Run server with stdio transport using ServerCore"""
    logger.info("Starting Supabase MCP server with stdio transport")
    
    try:
        # Get the FastMCP instance from core
        mcp = core.mcp_server
        
        logger.debug("Starting stdio transport")
        # Run with stdio transport
        mcp.run(transport="stdio")
        logger.debug("Stdio transport started successfully")
    except Exception as e:
        logger.error(f"Server error: {str(e)}")
        raise

def run_server_sse(core: ServerCore, host: str = "0.0.0.0", port: int = 8123) -> None:
    """Run server with SSE transport using ServerCore"""
    logger.info(f"Starting Supabase MCP server with SSE transport on {host}:{port}")
    
    try:
        logger.debug("Starting SSE transport")
        # Create and run SSE transport with the MCP server
        from supabase_mcp.transport.sse import SSETransport
        sse_transport = SSETransport(core.mcp_server, host=host, port=port)
        sse_transport.run()
        logger.debug("SSE transport started successfully")
    except Exception as e:
        logger.error(f"SSE Server error: {str(e)}")
        logger.exception("Full traceback:")
        raise
    finally:
        logger.info("Shutting down services")
        core.services.shutdown_services()

def run_server() -> None:
    # Create argument parser
    parser = argparse.ArgumentParser(description="Supabase MCP Server")
    parser.add_argument("--transport", choices=["stdio", "sse"], default="stdio", 
                        help="Transport type (default: stdio)")
    parser.add_argument("--host", default="0.0.0.0", 
                        help="Host for SSE server (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=8123, 
                        help="Port for SSE server (default: 8123)")

    # Parse arguments
    args = parser.parse_args()
    
    # Initialize core once
    core = ServerCore(settings)
    
    if args.transport == "sse":
        run_server_sse(core, args.host, args.port)
    else:
        run_server_stdio(core)

def run_inspector() -> None:
    """Inspector mode - same as mcp dev"""
    logger.info("Starting Supabase MCP server inspector")
    from mcp.cli.cli import dev
    return dev(__file__)

if __name__ == "__main__":
    logger.info("Starting Supabase MCP server")
    run_server()
