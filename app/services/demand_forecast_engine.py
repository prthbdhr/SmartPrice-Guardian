from typing import Dict

from app.utils.data_loader import (
    get_sales_by_sku,
    load_inventory
)


def forecast_demand(sku: str, window_days: int = 7) -> Dict:
    """
    Demand forecast using Simple Moving Average.
    Predicts demand for the next `window_days`.
    """

    # ---- Load data ----
    sales = get_sales_by_sku(sku)
    if not sales:
        raise ValueError("SKU not found in sales data")

    inventory = load_inventory()
    current_stock = inventory.get(sku)
    if current_stock is None:
        raise ValueError("SKU not found in inventory data")

    # ---- Step 1: Get recent sales ----
    recent_sales = sales[-window_days:]
    if not recent_sales:
        raise ValueError("Insufficient sales data for forecasting")

    recent_quantities = [item["quantity"] for item in recent_sales]

    # ---- Step 2: Predict next 7 days ----
    avg_recent_sales = sum(recent_quantities) / len(recent_quantities)
    predicted_demand = round(avg_recent_sales * window_days)

    # ---- Step 3: Risk Classification ----
    if predicted_demand > current_stock:
        risk = "STOCKOUT_RISK"
        explanation = (
            "Recent sales trend indicates demand will exceed available stock "
            "within the next 7 days."
        )

    elif predicted_demand < current_stock * 0.3:
        risk = "DEAD_STOCK_RISK"
        explanation = (
            "Forecasted demand is significantly lower than available inventory, "
            "indicating potential dead stock risk."
        )

    else:
        risk = "NORMAL"
        explanation = (
            "Forecasted demand is aligned with current inventory levels, "
            "indicating no immediate supply risk."
        )

    # ---- Output (LOCKED FORMAT) ----
    return {
        "sku": sku,
        "forecast_window_days": window_days,
        "predicted_demand": predicted_demand,
        "current_stock": current_stock,
        "risk": risk,
        "explanation": explanation
    }
