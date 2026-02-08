from typing import Dict, List

from app.services.pricing_engine import pricing_decision
from app.services.demand_forecast_engine import forecast_demand
from app.utils.data_loader import load_inventory

# at phase 5 depends on market trend computation
from app.services.market_trends import get_market_trend

market_trend = get_market_trend(category="electronics")
trend_line = f"Market context: {market_trend['impact']}"


def _detect_intent(question: str) -> str:
    q = question.lower()
    if "discount" in q or "price" in q:
        return "PRICING"
    if "restock" in q or "inventory" in q:
        return "INVENTORY"
    return "GENERAL"


def copilot_decision(sku: str, question: str) -> Dict:
    # ---- Step 1: Intent detection ----
    intent = _detect_intent(question)

    # ---- Step 2: Fetch system context (REAL DATA ONLY) ----
    pricing = pricing_decision(sku)
    forecast = forecast_demand(sku)
    inventory = load_inventory().get(sku)

    if inventory is None:
        raise ValueError("SKU not found in inventory")

    # ---- Step 3: Decision synthesis (NO HALLUCINATION) ----
    signals_used: List[str] = ["PRICING", "FORECAST", "INVENTORY"]

    pricing_dec = pricing["decision"]
    forecast_risk = forecast["risk"]

    # ---- Discount decision logic ----
    if intent == "PRICING":
        if forecast_risk == "STOCKOUT_RISK":
            decision = "DO_NOT_DISCOUNT"
            confidence = 0.92
            answer = (
                "No. Demand is outpacing inventory and stockout risk is high. "
                "Upcoming festive demand may further increase pressure. "
                "Discounting now would reduce margin without increasing sales."
            )

        elif forecast_risk == "DEAD_STOCK_RISK":
            # Use pricing engine decision to differentiate severity
            if pricing_dec == "STRONG_DISCOUNT":
                decision = "STRONG_DISCOUNT"
                confidence = 0.88
                answer = (
                    "Yes. Inventory has significantly outpaced demand for an extended period. "
                    "A strong discount is recommended to free cash and reduce prolonged holding costs."
                )
            else:
                decision = "MILD_DISCOUNT"
                confidence = 0.7
                answer = (
                    "A mild discount may help improve sales velocity, but aggressive discounting is not necessary yet. "
                    "Upcoming festive demand suggests waiting before taking stronger action."
                )

        else:  # NORMAL / borderline
            decision = "MILD_DISCOUNT"
            confidence = 0.7
            answer = (
                "A mild discount may help improve sales velocity, but aggressive discounting is not necessary yet. "
                "Monitor demand over the next few days."
            )

    else:
        decision = "NO_ACTION"
        confidence = 0.6
        answer = (
            "Based on current demand and inventory signals, no immediate action is required."
        )

    # ---- Locked response format ----
    return {
        "sku": sku,
        "decision": decision,
        "answer": answer,
        "confidence": confidence,
        "signals_used": signals_used
    }
