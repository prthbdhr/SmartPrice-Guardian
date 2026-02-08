from typing import Dict

from app.utils.data_loader import (
    get_sales_by_sku,
    load_inventory,
    load_competitor_prices
)


def pricing_decision(sku: str) -> Dict:
    # ---- Load data ----
    sales = get_sales_by_sku(sku)
    if not sales:
        raise ValueError("SKU not found in sales data")

    inventory = load_inventory()
    competitor_prices = load_competitor_prices()

    # ---- Compute signals ----
    total_units_sold = sum(item["quantity"] for item in sales)
    avg_daily_sales = total_units_sold / len(sales)

    current_stock = inventory.get(sku)
    if current_stock is None:
        raise ValueError("SKU not found in inventory data")

    days_of_stock = current_stock / avg_daily_sales if avg_daily_sales > 0 else float("inf")

    print("DEBUG SKU:", sku)
    print("DEBUG avg_daily_sales:", avg_daily_sales)
    print("DEBUG current_stock:", current_stock)
    print("DEBUG days_of_stock:", days_of_stock)


    current_price = sales[-1]["price"]
    competitor_price = competitor_prices.get(sku)

    # ---- Pricing Logic ----

    # 🔴 STOCKOUT RISK
    if days_of_stock < 3:
        recommended_price = round(current_price * 1.10, 2)  # 10% increase
        decision = "INCREASE"
        confidence = 0.9
        reason = (
            "High demand and critically low inventory indicate an imminent stockout. "
            "Demand exceeds supply, and increasing price helps protect margin while restocking."
        )

    # 🔵 DEAD / OVERSTOCK HANDLING (REFINED)
    elif days_of_stock > 45:
        recommended_price = round(current_price * 0.82, 2)  # ~18% discount
        decision = "STRONG_DISCOUNT"
        confidence = 0.88
        reason = (
            "Very low demand relative to inventory indicates severe overstock. "
            "Strong discount recommended to free up cash and reduce holding costs."
        )

    elif 30 <= days_of_stock <= 45:
        recommended_price = round(current_price * 0.93, 2)  # ~7% discount
        decision = "DISCOUNT"
        confidence = 0.68
        reason = (
            "Demand is weaker than inventory levels suggest. "
            "A mild discount can help improve sales velocity without sacrificing margin heavily."
        )

    # 🟡 NORMAL
    else:
        if competitor_price is not None and competitor_price < current_price:
            recommended_price = current_price
            decision = "HOLD"
            confidence = 0.65
            reason = (
                "Competitor pricing is lower, but demand and inventory are within acceptable ranges. "
                "Holding price avoids unnecessary margin erosion."
            )
        else:
            recommended_price = round(current_price * 1.025, 2)  # 2.5% increase
            decision = "INCREASE"
            confidence = 0.7
            reason = (
                "Demand and inventory are balanced with no significant competitive pressure. "
                "A slight price increase is recommended to improve margins."
            )

    # ---- Output (LOCKED FORMAT) ----
    return {
        "sku": sku,
        "current_price": current_price,
        "recommended_price": recommended_price,
        "decision": decision,
        "confidence": confidence,
        "reason": reason
    }
