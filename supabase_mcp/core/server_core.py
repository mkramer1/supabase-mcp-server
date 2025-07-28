from supabase_mcp.core.container import ServicesContainer
from supabase_mcp.settings import Settings
from supabase_mcp.exceptions import ToolNotFoundError

# Import ToolRegistry locally to avoid circular imports

class ServerCore:
    """Central core for Supabase MCP server functionality"""
    
    def __init__(self, settings: Settings):
        """
        Initialize the server core with services and tools
        
        Args:
            settings: Application settings
        """
        self.services = ServicesContainer()
        self.services.initialize_services(settings)
        
        from supabase_mcp.tools.registry import ToolRegistry
        # Create a FastMCP instance
        from mcp.server.fastmcp import FastMCP
        mcp_server = FastMCP()
        self.tool_registry = ToolRegistry(mcp_server, self.services)
        self.tool_registry.register_tools()
        
        # Store the FastMCP instance
        self.mcp_server = mcp_server
    
    async def get_tools(self) -> list:
        """Get all registered tools"""
        tools = await self.mcp_server.list_tools()
        return tools
    
    async def execute_tool(self, tool_name: str, arguments: dict) -> any:
        """
        Execute a tool by name with the given arguments
        
        Args:
            tool_name: Name of the tool to execute
            arguments: Dictionary of arguments for the tool
            
        Returns:
            Result of the tool execution
            
        Raises:
            ToolNotFoundError: If the tool doesn't exist
        """
        # Get the tool from FastMCP
        tool = self.mcp_server.get_tool(tool_name)
        if not tool:
            raise ToolNotFoundError(f"Tool '{tool_name}' not found")
            
        # Execute the tool
        return await tool.function(**arguments)
