# app/services/market_trends.py

RAW_TRENDS = [
    {
        "category": "electronics",
        "signal": "Festive season approaching",
        "expected_impact": "increase"
    },
    {
        "category": "home_appliances",
        "signal": "Summer season demand",
        "expected_impact": "increase"
    },
    {
        "category": "general",
        "signal": "Economic slowdown concerns",
        "expected_impact": "decrease"
    }
]


def summarize_trend(trend: dict) -> str:
    if trend["expected_impact"] == "increase":
        return f"{trend['signal']}. Demand likely to increase."
    else:
        return f"{trend['signal']}. Demand may soften."


def get_market_trend(category: str = "general") -> dict:
    """
    Returns ONE market trend signal relevant to the category.
    Fallbacks to 'general'.
    """
    for trend in RAW_TRENDS:
        if trend["category"] == category:
            return {
                "signal": trend["signal"],
                "impact": summarize_trend(trend),
                "confidence": 0.75
            }

    # fallback
    trend = RAW_TRENDS[-1]
    return {
        "signal": trend["signal"],
        "impact": summarize_trend(trend),
        "confidence": 0.7
    }
