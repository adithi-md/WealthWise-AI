ALLOWED_KEYWORDS = [
    "mutual fund", "sip", "investment",
    "stock", "shares", "equity", "nav", "returns"
]

def is_allowed(query):
    return any(word in query.lower() for word in ALLOWED_KEYWORDS)
