HIGH_KEYWORDS = [
    "emergency", "fire", "danger", "security threat", "accident", "medical",
    "urgent", "no electricity", "no water", "leakage", "spark", "theft",
    "suspicious", "immediate", "hazard"
]

MEDIUM_KEYWORDS = [
    "not working", "broken", "damaged", "repeated", "slow", "low pressure",
    "disconnection", "malfunction", "faulty", "noise"
]

LOW_KEYWORDS = [
    "suggestion", "request", "feedback", "inquiry", "would like",
    "recommend", "minor", "general"
]

def detect_priority(text: str) -> str:
    t = text.lower()

    for kw in HIGH_KEYWORDS:
        if kw in t:
            return "HIGH"

    for kw in MEDIUM_KEYWORDS:
        if kw in t:
            return "MEDIUM"

    for kw in LOW_KEYWORDS:
        if kw in t:
            return "LOW"

    return "MEDIUM"
