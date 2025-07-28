import asyncio
from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp.shared.message import SessionMessage
from mcp.types import JSONRPCRequest

async def test_server():
    server_params = StdioServerParameters(
        command="python",
        args=["-m", "supabase_mcp.main", "--transport", "stdio"]
    )
    
    async with stdio_client(server_params) as (read_stream, write_stream):
        # Prepare JSON-RPC request with correct method name
        request = JSONRPCRequest(
            jsonrpc="2.0",
            method="tools/call",
            params={
                "server_name": "supabase-mcp-server-stdio",
                "tool_name": "get_schemas",
                "arguments": {}
            },
            id=1
        )
        
        # Create SessionMessage
        message = SessionMessage(message=request)
        
        # Send tool call
        await write_stream.send(message)
        
        # Receive response
        response = await read_stream.receive()
        print("Tool response:", response)

if __name__ == "__main__":
    asyncio.run(test_server())
