
import json
import os

import logging

logger = logging.getLogger(__name__)

from dotenv import load_dotenv
from fastapi import HTTPException
from groq import AsyncGroq

from database.connection import SessionLocal
from database.models import ChatHistory

from ..mcp_client import call_mcp_tool
from ..rag_client import search_rag
from .schema.chat_schema import ChatRequest, ChatResponse


load_dotenv()

groq_client = AsyncGroq(api_key=os.environ["GROQ_API_KEY"])
MODEL_NAME = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_account_balance",
            "description": (
                "Get the balance and account type for a demo banking account. "
                "Use DEMO001 if the user does not specify an account ID. "
                "Never invent another account ID."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "account_id": {
                        "type": "string",
                        "description": "Demo account ID, such as DEMO001",
                    }
                },
                "required": ["account_id"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_recent_transactions",
            "description": (
                "Get recent transactions for a demo banking account. "
                "Use DEMO001 if the user does not specify an account ID. "
                "Never invent another account ID."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "account_id": {
                        "type": "string",
                        "description": "Demo account ID, such as DEMO001",
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Number of transactions, from 1 to 10",
                    },
                },
                "required": ["account_id", "limit"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_banking_policy",
            "description": (
                "Search banking policy documents and generate a grounded answer. "
                "Use this for complaints, customer rights, policy rules, "
                "and document-related questions."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The user's banking policy question",
                    }
                },
                "required": ["query"],
                "additionalProperties": False,
            },
        },
    },
]


SYSTEM_PROMPT = """
You are an assistant for a banking demo application.

Choose tools based on the user's intent:
- Account balance questions: get_account_balance.
- Recent transaction questions: get_recent_transactions.
- Banking policy and document questions: search_banking_policy.

Use the tools for factual banking data and policy answers.
Do not invent balances, transactions, or policy rules.
For demo account queries, use DEMO001 if no account ID is specified.
The banking tools return mock data for demonstration, not real customer data.
Answer clearly using the tool results.
"""


async def execute_tool(name: str, arguments: dict) -> str:
    """Execute only the tools explicitly supported by this Agent."""

    if name == "get_account_balance":
        account_id = arguments.get("account_id", "DEMO001")
        if not isinstance(account_id, str) or not account_id.strip():
            raise ValueError("A valid account_id is required.")

        return await call_mcp_tool(
            "get_account_balance",
            {"account_id": account_id},
        )

    if name == "get_recent_transactions":
        account_id = arguments.get("account_id", "DEMO001")
        limit = arguments.get("limit", 5)

        if not isinstance(account_id, str) or not account_id.strip():
            raise ValueError("A valid account_id is required.")

        if type(limit) is not int or not 1 <= limit <= 10:
            raise ValueError("Transaction limit must be between 1 and 10.")

        return await call_mcp_tool(
            "get_recent_transactions",
            {"account_id": account_id, "limit": limit},
        )

    if name == "search_banking_policy":
        query = arguments.get("query")
        if not isinstance(query, str) or not query.strip():
            raise ValueError("A policy search query is required.")

        result = await search_rag(query, top_k=3)
        return json.dumps(result)

    raise ValueError(f"Unsupported tool: {name}")


class ChatService:
    async def chat(self, request: ChatRequest) -> ChatResponse:
        try:
            messages = [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": request.message},
            ]

            # Allow a few tool-calling rounds, then return the final answer.
            for _ in range(4):
                completion = await groq_client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=messages,
                    tools=TOOLS,
                    tool_choice="auto",
                    temperature=0.2,
                    max_completion_tokens=800,
                )

                assistant_message = completion.choices[0].message
                tool_calls = assistant_message.tool_calls

                if not tool_calls:
                    response_text = assistant_message.content
                    if not response_text:
                        response_text = (
                            "I couldn't generate a response for that request."
                        )
                    break

                messages.append(
                    {
                        "role": "assistant",
                        "content": assistant_message.content,
                        "tool_calls": [
                            call.model_dump(exclude_none=True)
                            for call in tool_calls
                        ],
                    }
                )

                for tool_call in tool_calls:
                    tool_name = tool_call.function.name
                    arguments = json.loads(tool_call.function.arguments or "{}")

                    result = await execute_tool(tool_name, arguments)

                    messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": result,
                        }
                    )
            else:
                response_text = (
                    "I couldn't complete the request after several tool calls."
                )

        except (ValueError, json.JSONDecodeError) as exc:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid tool request: {exc}",
            ) from exc
        except HTTPException:
            raise
        except Exception as exc:
            logger.exception("Agent chat request failed")
            raise HTTPException(
                status_code=502,
                detail="The Agent could not complete the request.",
            ) from exc

        # Preserve the existing chat-history persistence.
        with SessionLocal() as db:
            try:
                chat_record = ChatHistory(
                    user_message=request.message,
                    agent_response=response_text,
                    status="completed",
                )
                db.add(chat_record)
                db.commit()
            except Exception:
                db.rollback()
                raise

        return ChatResponse(response=response_text)
