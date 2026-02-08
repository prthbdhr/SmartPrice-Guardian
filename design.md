# SmartPrice Guardian — Design Document

## 1. Overview
SmartPrice Guardian is an AI-powered backend system designed to help retailers make **clear, explainable, and data-driven pricing and inventory decisions**.  
The system focuses on *decisions*, not dashboards, and answers questions like:
- Should I discount today?
- Is there a stockout risk?
- Which products are dead stock?

---

## 2. Design Goals
- **Explainability first**: Every decision must have a reason and confidence.
- **Deterministic logic**: No black-box ML in critical paths.
- **Modular architecture**: Each intelligence layer is isolated.
- **Demo-safe & judge-friendly**: Predictable, consistent behavior.
- **Plug-in extensibility**: Future ML, DB, or APIs can be added without refactor.

---

## 3. System Architecture

### High-Level Flow
```
Sales & Inventory Data
        ↓
Pricing Engine + Demand Forecast Engine
        ↓
Market Trend Signals
        ↓
AI Decision Copilot
        ↓
Clear Business Action
```

Each layer strengthens the next. No layer overrides core signals.

---

## 4. Data Layer
**Source:** CSV files (sales, inventory, competitor prices)

**Responsibilities:**
- Load clean data
- Filter by SKU
- Provide structured Python objects

**Design Choice:**  
CSV-based input keeps the system lightweight and demo-ready while maintaining realistic constraints.

---

## 5. Pricing Engine (Phase 2)

### Core Signals
- Average daily sales
- Current stock
- Days of stock remaining
- Competitor price

### Decision Rules
- **STOCKOUT_RISK (< 3 days):** Increase price (8–12%)
- **DEAD_STOCK (> 45 days):** Strong discount (15–20%)
- **OVERSTOCK (30–45 days):** Mild discount (5–8%)
- **NORMAL:** Hold or slight increase

**Why rules over ML?**  
Judges and stakeholders trust logic they can understand and defend.

---

## 6. Demand Forecast Engine (Phase 3)

### Strategy
- Simple Moving Average (last 7 days)
- Predict next 7 days of demand

### Risk Classification
- Predicted demand > stock → STOCKOUT_RISK
- Predicted demand < 30% of stock → DEAD_STOCK_RISK
- Else → NORMAL

**Key Principle:**  
Consistency and actionability matter more than raw accuracy.

---

## 7. AI Decision Copilot (Phase 4)

### Purpose
Translate system intelligence into **natural-language business decisions**.

### Characteristics
- Not a chatbot
- Not a data explainer
- Fully grounded in system outputs

### Inputs
- Pricing decision
- Demand forecast
- Inventory status
- Market trends

### Output
- Clear decision
- Short explanation (≤ 3 sentences)
- Confidence score
- Signals used

---

## 8. Market Trends Module (Phase 5)

### Strategy
- Hardcoded, scenario-based trends
- Optional LLM or rule-based summarization

### Role
- Provide *context*, not control
- Nudge decisions without overriding core logic

Example:
> Festive season approaching → demand likely to increase

---

## 9. API Design

### Key Endpoints
- `/pricing/recommendation/{sku}`
- `/forecast/{sku}`
- `/copilot/query`
- `/market/trends`

**Design Principle:**  
Routes are thin. All intelligence lives in services.

---

## 10. Deployment

- **Framework:** FastAPI
- **Containerization:** Docker (single-container)
- **Docs:** Auto-generated Swagger (`/docs`)

The system is production-deployable and cloud-ready.

---

## 11. Non-Goals
- No real-time scraping
- No black-box ML models
- No heavy dashboards
- No over-automation

These are intentionally deferred to keep the system focused.

---

## 12. Future Extensions
- Replace CSV with database
- Add real-time competitor scraping
- Introduce ML-based forecasting
- Role-based decision personalization

---

## 13. Summary
SmartPrice Guardian demonstrates how **AI-driven reasoning**, when designed carefully, can outperform complex dashboards by delivering **clear, explainable business actions**.

> Data → Signals → Decisions
