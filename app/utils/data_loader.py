import csv
from pathlib import Path

# Base data directory (project-root/data)
BASE_DATA_DIR = Path(__file__).resolve().parents[2] / "data"


def load_sales_data():
    """
    Load sales.csv and return a list of dicts:
    [
        {
            "date": "2025-01-01",
            "sku": "SKU-A",
            "quantity": 5,
            "price": 1200
        },
        ...
    ]
    """
    sales_file = BASE_DATA_DIR / "sales.csv"
    sales_data = []

    with open(sales_file, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            sales_data.append({
                "date": row["date"],
                "sku": row["sku"],
                "quantity": int(row["quantity"]),
                "price": float(row["price"])
            })

    return sales_data


def load_inventory():
    """
    Load inventory.csv and return a dict:
    {
        "SKU-A": 10,
        "SKU-B": 200,
        ...
    }
    """
    inventory_file = BASE_DATA_DIR / "inventory.csv"
    inventory = {}

    with open(inventory_file, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            inventory[row["sku"]] = int(row["stock"])

    return inventory


def load_competitor_prices():
    """
    Load competitor_prices.csv and return a dict:
    {
        "SKU-A": 1200,
        "SKU-B": 780,
        ...
    }
    """
    competitor_file = BASE_DATA_DIR / "competitor_prices.csv"
    competitor_prices = {}

    with open(competitor_file, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            competitor_prices[row["sku"]] = float(row["price"])

    return competitor_prices


def get_sales_by_sku(sku):
    """
    Filter sales data for a single SKU.
    Returns a list sorted by date.
    """
    sales_data = load_sales_data()
    sku_sales = [row for row in sales_data if row["sku"] == sku]

    # Sorting keeps downstream logic simple and predictable
    sku_sales.sort(key=lambda x: x["date"])

    return sku_sales
