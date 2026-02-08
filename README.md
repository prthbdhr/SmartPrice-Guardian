# 🚀 SmartPrice Guardian  
**AI-Powered Pricing & Decision Intelligence for Retailers**

SmartPrice Guardian is an AI-driven backend system that helps retailers and marketplace sellers make **clear, data-backed pricing and inventory decisions** by combining historical sales data, demand forecasting, market trends, and an AI decision copilot.

Unlike generic dashboards, SmartPrice Guardian tells sellers **exactly what to do and why**.

---

## 🧠 What Problem Does This Solve?

Retailers often struggle with:
- Over-discounting high-demand products
- Holding dead stock for too long
- Missing demand spikes due to seasonality
- Making pricing decisions based on intuition instead of data

**SmartPrice Guardian replaces guesswork with explainable decisions.**

---

## ✨ Key Features

### 📊 Pricing Intelligence
- Recommends **price increase, hold, or discount**
- Considers demand, inventory, and competitor pricing
- Provides confidence scores and human-readable reasoning

### 🔮 Demand Forecasting
- Predicts near-term demand (7-day window)
- Classifies SKUs into:
  - `STOCKOUT_RISK`
  - `OVERSTOCK_RISK`
  - `DEAD_STOCK_RISK`

### 🤖 AI Decision Copilot
- Answers business questions like:
  > *"Should I discount today?"*
- Responses are:
  - Short
  - Decisive
  - Grounded in system data (not generic AI talk)

### 🌍 Market Trend Awareness
- Incorporates external signals (e.g., festive season demand)
- Nudges decisions without overriding core data

---

## 🏗️ System Architecture

```
Sales & Inventory Data
        ↓
Pricing Engine ←→ Demand Forecast Engine
        ↓
Market Trend Signals
        ↓
AI Decision Copilot
        ↓
Clear Business Action
```

---

## 📦 Tech Stack

- **Backend:** FastAPI
- **AI Logic:** Rule-based intelligence + LLM-assisted reasoning
- **Forecasting:** Moving average demand prediction
- **Data:** CSV-based mock retail data
- **Deployment:** Docker

---

## 🔗 API Endpoints Overview

| Endpoint | Description |
|----------|-------------|
| `/data/summary/{sku}` | SKU sales & inventory summary |
| `/pricing/recommendation/{sku}` | Pricing decision with reasoning |
| `/forecast/{sku}` | Demand forecast & risk classification |
| `/copilot/query` | AI decision copilot |
| `/market/trends` | External market trend signals |

---

## 📘 API Documentation (Swagger)

Once the app is running, interactive API docs are available at:
```
http://localhost:8000/docs
```

Judges can directly test all endpoints from the browser.

---

## 🐳 Run with Docker

### Build the image
```bash
docker build -t smartprice-backend .
```

### Run the container
```bash
docker run -p 8000:8000 smartprice-backend
```

The API will be available at:
```
http://localhost:8000
```

---

## 🧪 Example Copilot Output

**Question:**
```
Should I discount today?
```

**Answer (Stockout Case):**
```
No. Demand is outpacing inventory and stockout risk is high. 
Discounting now would reduce margin without increasing sales. 
Reassess after restocking.
```

---

## 🎯 Why This Matters

SmartPrice Guardian demonstrates how AI can:
- Improve profitability
- Reduce inventory waste
- Support confident business decisions

All without requiring complex ML pipelines or black-box models.

---

## 🚀 Future Enhancements

- Live marketplace price ingestion
- Multi-store SKU analysis
- Frontend dashboard for sellers
- Real-time trend integration

---

## 👨‍💻 Built For

Hackathons, retail intelligence demos, and showcasing practical AI decision systems with real commercial value.

---


