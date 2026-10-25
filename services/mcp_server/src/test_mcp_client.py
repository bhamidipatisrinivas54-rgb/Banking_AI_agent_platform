
import asyncio

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client


async def main():
    url = "http://127.0.0.1:8003/mcp"

    async with streamablehttp_client(url) as (
        read_stream,
        write_stream,
        _,
    ):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            # List the tools registered with the MCP server
            result = await session.list_tools()

            print("\nAvailable MCP tools:")
            for tool in result.tools:
                print(f"- {tool.name}: {tool.description}")

            # Test the balance tool
            print("\nTesting get_account_balance:")
            balance = await session.call_tool(
                "get_account_balance",
                {"account_id": "DEMO001"},
            )
            print(balance)

            # Test the transactions tool
            print("\nTesting get_recent_transactions:")
            transactions = await session.call_tool(
                "get_recent_transactions",
                {"account_id": "DEMO001", "limit": 3},
            )
            print(transactions)


if __name__ == "__main__":
    asyncio.run(main())
