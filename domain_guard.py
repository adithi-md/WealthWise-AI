# domain_guard.py

MUTUAL_FUND_KEYWORDS = [
    "mutual fund",
    "mutual funds",
    "sip",
    "systematic investment plan",
    "nav",
    "expense ratio",
    "equity fund",
    "debt fund",
    "hybrid fund",
    "index fund",
    "elss",
    "fund manager",
    "aum",
    "portfolio",
    "returns",
    "risk",
    "long term investment",
    "diversification",
    "lumpsum",
    "market risk",
    "investment",
    "invest",
    "fund",
    "scheme",
    "amc",
    "asset management",
    "wealth",
    "savings",
    "retirement",
    "goal",
    "financial planning",
    "compounding",
    "dividend",
    "growth",
    "direct plan",
    "regular plan",
    "exit load",
    "redemption",
    "units",
    "folio"
]

FORBIDDEN_KEYWORDS = [
    "stock",
    "share",
    "crypto",
    "bitcoin",
    "ethereum",
    "forex",
    "trading",
    "day trade",
    "options",
    "futures",
    "derivative",
    "real estate",
    "property",
    "gold",
    "commodity",
    "loan",
    "credit card",
    "mortgage"
]


def is_mutual_fund_query(user_query: str) -> bool:
    """
    NLP-based domain check to verify whether
    the query is related to mutual funds.
    Returns False if forbidden topics are detected.
    """
    query = user_query.lower()
    
    # Check for forbidden topics first
    for forbidden in FORBIDDEN_KEYWORDS:
        if forbidden in query:
            return False

    # Check for mutual fund keywords
    for keyword in MUTUAL_FUND_KEYWORDS:
        if keyword in query:
            return True

    # Allow general greetings and conversational queries
    greetings = ["hello", "hi", "hey", "help", "what can you", "who are you", "thanks", "thank you"]
    for greeting in greetings:
        if greeting in query:
            return True

    return False
