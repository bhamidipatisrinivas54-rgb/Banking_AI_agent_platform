
import asyncio
import json

from services.agent.src.mcp_client import (
    list_mcp_tools,
    call_mcp_tool,
)


async def main():
    # 1. Discover available tools
    tools = await list_mcp_tools()

    print("Available tools:")
    for tool in tools:
        print(f"- {tool['name']}")

    # 2. Execute the balance tool
    print("\nCalling get_account_balance...")
    result = await call_mcp_tool(
        "get_account_balance",
        {"account_id": "DEMO001"},
    )

    print("Tool result:")
    print(json.dumps(json.loads(result), indent=2))


if __name__ == "__main__":
    asyncio.run(main())
