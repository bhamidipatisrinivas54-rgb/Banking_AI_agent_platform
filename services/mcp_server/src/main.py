
from mcp.server.fastmcp import FastMCP

from services.mcp_server.src.tools.banking_tools import (
    get_account_balance as fetch_account_balance,
    get_recent_transactions as fetch_recent_transactions,
)


mcp = FastMCP(
    "Banking Demo MCP Server",
    json_response=True,
    host="127.0.0.1",
    port=8003,
    streamable_http_path="/mcp",
)


@mcp.tool()
def get_account_balance(account_id: str) -> dict:
    """Get the balance and account type for a predefined demo account.

    Args:
        account_id: Demo account identifier, such as DEMO001 or DEMO002.
    """
    return fetch_account_balance(account_id)


@mcp.tool()
def get_recent_transactions(
    account_id: str,
    limit: int = 5,
) -> dict:
    """Get recent mock transactions for a predefined demo account.

    Args:
        account_id: Demo account identifier, such as DEMO001 or DEMO002.
        limit: Maximum number of transactions to return, between 1 and 10.
    """
    return fetch_recent_transactions(account_id, limit)


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
