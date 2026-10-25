
from datetime import datetime, timedelta, timezone


# Mock data for development only.
DEMO_ACCOUNTS = {
    "DEMO001": {
        "account_type": "Savings",
        "balance": 25450.75,
        "currency": "INR",
    },
    "DEMO002": {
        "account_type": "Current",
        "balance": 187900.00,
        "currency": "INR",
    },
}

DEMO_TRANSACTIONS = {
    "DEMO001": [
        {
            "transaction_id": "TXN1001",
            "description": "Grocery purchase",
            "amount": -1250.00,
            "currency": "INR",
            "days_ago": 1,
        },
        {
            "transaction_id": "TXN1002",
            "description": "Salary credit",
            "amount": 45000.00,
            "currency": "INR",
            "days_ago": 3,
        },
        {
            "transaction_id": "TXN1003",
            "description": "Electricity bill",
            "amount": -1800.00,
            "currency": "INR",
            "days_ago": 5,
        },
    ],
    "DEMO002": [
        {
            "transaction_id": "TXN2001",
            "description": "Vendor payment",
            "amount": -15000.00,
            "currency": "INR",
            "days_ago": 1,
        },
        {
            "transaction_id": "TXN2002",
            "description": "Customer payment",
            "amount": 50000.00,
            "currency": "INR",
            "days_ago": 2,
        },
    ],
}


def get_account_balance(account_id: str) -> dict:
    """Return the mock balance for a predefined demo account."""
    account = DEMO_ACCOUNTS.get(account_id)

    if account is None:
        return {
            "success": False,
            "message": "Demo account not found.",
        }

    return {
        "success": True,
        "account_id": account_id,
        **account,
    }


def get_recent_transactions(
    account_id: str,
    limit: int = 5,
) -> dict:
    """Return recent mock transactions for a predefined demo account."""
    if account_id not in DEMO_ACCOUNTS:
        return {
            "success": False,
            "message": "Demo account not found.",
        }

    if not 1 <= limit <= 10:
        return {
            "success": False,
            "message": "Limit must be between 1 and 10.",
        }

    now = datetime.now(timezone.utc)
    transactions = []

    for transaction in DEMO_TRANSACTIONS.get(account_id, [])[:limit]:
        transaction_date = now - timedelta(
            days=transaction["days_ago"]
        )

        transactions.append({
            "transaction_id": transaction["transaction_id"],
            "description": transaction["description"],
            "amount": transaction["amount"],
            "currency": transaction["currency"],
            "date": transaction_date.isoformat(),
        })

    return {
        "success": True,
        "account_id": account_id,
        "transactions": transactions,
    }
