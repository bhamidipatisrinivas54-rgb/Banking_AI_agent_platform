
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client


MCP_SERVER_URL = "http://127.0.0.1:8003/mcp"


async def list_mcp_tools():
    """Connect to the MCP server and list its available tools."""
    async with streamablehttp_client(MCP_SERVER_URL) as (
        read_stream,
        write_stream,
        _,
    ):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            result = await session.list_tools()

            return [
                {
                    "name": tool.name,
                    "description": tool.description,
                }
                for tool in result.tools
            ]


async def call_mcp_tool(tool_name: str, arguments: dict) -> str:
    """Execute a registered MCP tool and return its text result."""
    async with streamablehttp_client(MCP_SERVER_URL) as (
        read_stream,
        write_stream,
        _,
    ):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            result = await session.call_tool(
                tool_name,
                arguments,
            )

            if result.isError:
                raise RuntimeError(
                    f"MCP tool '{tool_name}' returned an error"
                )

            return "\n".join(
                item.text
                for item in result.content
                if hasattr(item, "text")
            )
