from fastapi import APIRouter, HTTPException

from app.utils.data_loader import (
    get_sales_by_sku,
    load_inventory,
    load_competitor_prices
)

router = APIRouter(prefix="/data", tags=["Data Summary"])


@router.get("/summary/{sku}")
def get_data_summary(sku: str):
    sales = get_sales_by_sku(sku)

    if not sales:
        raise HTTPException(status_code=404, detail="SKU not found in sales data")

    total_units_sold = sum(item["quantity"] for item in sales)
    avg_daily_sales = round(total_units_sold / len(sales), 2)

    inventory = load_inventory()
    competitor_prices = load_competitor_prices()

    return {
        "sku": sku,
        "total_units_sold": total_units_sold,
        "avg_daily_sales": avg_daily_sales,
        "current_stock": inventory.get(sku),
        "competitor_price": competitor_prices.get(sku)
    }
