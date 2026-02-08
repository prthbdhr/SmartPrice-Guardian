# SmartPrice Guardian - System Requirements

## Overview

SmartPrice Guardian is an AI-powered pricing and decision intelligence system for retailers. This document outlines the functional and technical requirements for the system.

---

## 1. Functional Requirements

### 1.1 Data Summary Service

**Purpose:** Provide aggregated sales and inventory metrics for individual SKUs.

**Requirements:**
- **FR-1.1.1:** System shall load and parse sales data from CSV files
- **FR-1.1.2:** System shall calculate total units sold per SKU
- **FR-1.1.3:** System shall calculate average daily sales per SKU
- **FR-1.1.4:** System shall retrieve current stock levels from inventory data
- **FR-1.1.5:** System shall retrieve competitor pricing information
- **FR-1.1.6:** System shall return 404 error for non-existent SKUs

**Endpoint:** `GET /data/summary/{sku}`

**Expected Output:**
```json
{
  "sku": "string",
  "total_units_sold": "number",
  "avg_daily_sales": "number",
  "current_stock": "number",
  "competitor_price": "number"
}
```

---

### 1.2 Pricing Recommendation Service

**Purpose:** Generate data-driven pricing recommendations with confidence scores and reasoning.

**Requirements:**
- **FR-1.2.1:** System shall analyze demand trends from historical sales data
- **FR-1.2.2:** System shall calculate days of stock remaining
- **FR-1.2.3:** System shall identify stockout risk (< 3 days of stock)
- **FR-1.2.4:** System shall identify overstock situations (30-45 days of stock)
- **FR-1.2.5:** System shall identify severe overstock (> 45 days of stock)
- **FR-1.2.6:** System shall recommend price increases for stockout scenarios
- **FR-1.2.7:** System shall recommend discounts for overstock scenarios
- **FR-1.2.8:** System shall consider competitor pricing in normal scenarios
- **FR-1.2.9:** System shall provide confidence scores (0.0 - 1.0)
- **FR-1.2.10:** System shall provide human-readable reasoning for each decision

**Endpoint:** `GET /pricing/recommendation/{sku}`

**Decision Types:**
- `INCREASE` - Price increase recommended
- `STRONG_DISCOUNT` - Aggressive discount needed
- `DISCOUNT` - Mild discount recommended
- `HOLD` - Maintain current price

**Expected Output:**
```json
{
  "sku": "string",
  "current_price": "number",
  "recommended_price": "number",
  "decision": "string",
  "confidence": "number",
  "reason": "string"
}
```

---

### 1.3 Demand Forecast Service

**Purpose:** Predict future demand and classify inventory risk levels.

**Requirements:**
- **FR-1.3.1:** System shall use Simple Moving Average (SMA) for demand prediction
- **FR-1.3.2:** System shall forecast demand for a 7-day window
- **FR-1.3.3:** System shall classify risk as STOCKOUT_RISK when predicted demand > current stock
- **FR-1.3.4:** System shall classify risk as DEAD_STOCK_RISK when predicted demand < 30% of stock
- **FR-1.3.5:** System shall classify risk as OVERSTOCK_RISK for moderate overstock
- **FR-1.3.6:** System shall classify risk as NORMAL when demand aligns with inventory
- **FR-1.3.7:** System shall provide explanations for risk classifications

**Endpoint:** `GET /forecast/{sku}`

**Risk Classifications:**
- `STOCKOUT_RISK` - Demand will exceed available stock
- `DEAD_STOCK_RISK` - Severe overstock, very low demand
- `OVERSTOCK_RISK` - Moderate overstock
- `NORMAL` - Balanced inventory levels

**Expected Output:**
```json
{
  "sku": "string",
  "forecast_window_days": "number",
  "predicted_demand": "number",
  "current_stock": "number",
  "risk": "string",
  "explanation": "string"
}
```

---

### 1.4 AI Decision Copilot Service

**Purpose:** Provide natural language answers to business questions using integrated system data.

**Requirements:**
- **FR-1.4.1:** System shall detect user intent from natural language questions
- **FR-1.4.2:** System shall integrate data from pricing, forecast, and inventory services
- **FR-1.4.3:** System shall provide decisive recommendations (not generic advice)
- **FR-1.4.4:** System shall recommend DO_NOT_DISCOUNT for stockout scenarios
- **FR-1.4.5:** System shall recommend STRONG_DISCOUNT for dead stock scenarios
- **FR-1.4.6:** System shall recommend MILD_DISCOUNT for overstock scenarios
- **FR-1.4.7:** System shall provide confidence scores appropriate to the scenario
- **FR-1.4.8:** System shall include reasoning grounded in actual data
- **FR-1.4.9:** System shall list all signals used in decision-making

**Endpoint:** `POST /copilot/query`

**Request Body:**
```json
{
  "sku": "string",
  "question": "string"
}
```

**Decision Types:**
- `DO_NOT_DISCOUNT` - Do not discount (stockout case)
- `STRONG_DISCOUNT` - Aggressive discount needed (dead stock)
- `MILD_DISCOUNT` - Cautious discount (overstock)
- `NO_ACTION` - No immediate action required

**Expected Output:**
```json
{
  "sku": "string",
  "decision": "string",
  "answer": "string",
  "confidence": "number",
  "signals_used": ["string"]
}
```

---

### 1.5 Market Trends Service

**Purpose:** Provide external market trend signals to enhance decision-making.

**Requirements:**
- **FR-1.5.1:** System shall identify current market trends (e.g., festive season)
- **FR-1.5.2:** System shall provide trend descriptions
- **FR-1.5.3:** System shall indicate trend impact on demand
- **FR-1.5.4:** System shall return multiple active trends when applicable

**Endpoint:** `GET /market/trends`

**Expected Output:**
```json
{
  "trends": [
    {
      "name": "string",
      "description": "string",
      "impact": "string"
    }
  ]
}
```

---

## 2. Data Requirements

### 2.1 Sales Data

**Format:** CSV file with columns: `date`, `sku`, `quantity`, `price`

**Requirements:**
- **DR-2.1.1:** Minimum 30 days of historical data per SKU
- **DR-2.1.2:** Daily granularity
- **DR-2.1.3:** Chronologically ordered data
- **DR-2.1.4:** Valid date format (YYYY-MM-DD)
- **DR-2.1.5:** Positive quantity values
- **DR-2.1.6:** Positive price values

### 2.2 Inventory Data

**Format:** CSV file with columns: `sku`, `stock`

**Requirements:**
- **DR-2.2.1:** Current stock levels for all active SKUs
- **DR-2.2.2:** Non-negative stock values
- **DR-2.2.3:** Unique SKU identifiers

### 2.3 Competitor Pricing Data

**Format:** CSV file with columns: `sku`, `price`

**Requirements:**
- **DR-2.3.1:** Competitor prices for all active SKUs
- **DR-2.3.2:** Positive price values
- **DR-2.3.3:** Unique SKU identifiers

---

## 3. Non-Functional Requirements

### 3.1 Performance

- **NFR-3.1.1:** API response time shall be < 500ms for single SKU queries
- **NFR-3.1.2:** System shall handle concurrent requests efficiently
- **NFR-3.1.3:** CSV data loading shall be optimized for quick access

### 3.2 Reliability

- **NFR-3.2.1:** System shall return appropriate HTTP status codes
- **NFR-3.2.2:** System shall handle missing SKUs gracefully (404 errors)
- **NFR-3.2.3:** System shall validate input data before processing
- **NFR-3.2.4:** System shall provide meaningful error messages

### 3.3 Maintainability

- **NFR-3.3.1:** Code shall follow FastAPI best practices
- **NFR-3.3.2:** Business logic shall be separated from API routing
- **NFR-3.3.3:** Data loading utilities shall be reusable
- **NFR-3.3.4:** System shall use type hints for better code clarity

### 3.4 Scalability

- **NFR-3.4.1:** System architecture shall support adding new data sources
- **NFR-3.4.2:** System shall support adding new decision rules
- **NFR-3.4.3:** System shall be containerized for easy deployment

### 3.5 Usability

- **NFR-3.5.1:** API shall provide interactive Swagger documentation
- **NFR-3.5.2:** All responses shall include human-readable explanations
- **NFR-3.5.3:** Confidence scores shall be clearly communicated
- **NFR-3.5.4:** Error messages shall be actionable

---

## 4. Technical Requirements

### 4.1 Technology Stack

- **TR-4.1.1:** Backend framework: FastAPI
- **TR-4.1.2:** Python version: 3.9+
- **TR-4.1.3:** Data format: CSV
- **TR-4.1.4:** Containerization: Docker
- **TR-4.1.5:** API documentation: OpenAPI/Swagger

### 4.2 Dependencies

- **TR-4.2.1:** FastAPI for API framework
- **TR-4.2.2:** Uvicorn for ASGI server
- **TR-4.2.3:** Pydantic for data validation
- **TR-4.2.4:** Python standard library for CSV parsing

### 4.3 Deployment

- **TR-4.3.1:** System shall run on port 8001
- **TR-4.3.2:** System shall be deployable via Docker
- **TR-4.3.3:** System shall include health check endpoint
- **TR-4.3.4:** System shall support hot reload in development

---

## 5. Business Rules

### 5.1 Pricing Logic

- **BR-5.1.1:** Stockout risk (< 3 days stock) → 10% price increase
- **BR-5.1.2:** Severe overstock (> 45 days stock) → 18% discount
- **BR-5.1.3:** Moderate overstock (30-45 days stock) → 7% discount
- **BR-5.1.4:** Normal conditions with no competitive pressure → 2.5% increase
- **BR-5.1.5:** Normal conditions with competitive pressure → hold price

### 5.2 Forecast Logic

- **BR-5.2.1:** Use 7-day moving average for demand prediction
- **BR-5.2.2:** Predict demand for next 7 days
- **BR-5.2.3:** Classify as STOCKOUT_RISK if predicted demand > current stock
- **BR-5.2.4:** Classify as DEAD_STOCK_RISK if predicted demand < 30% of stock

### 5.3 Copilot Logic

- **BR-5.3.1:** Prioritize forecast risk over pricing decision
- **BR-5.3.2:** Use pricing engine decision to differentiate discount severity
- **BR-5.3.3:** Provide high confidence (0.9+) for stockout scenarios
- **BR-5.3.4:** Provide high confidence (0.85+) for strong discount scenarios
- **BR-5.3.5:** Provide moderate confidence (0.7) for mild discount scenarios

---

## 6. Acceptance Criteria

### 6.1 System-Level

- **AC-6.1.1:** All API endpoints return valid JSON responses
- **AC-6.1.2:** Swagger documentation is accessible at `/docs`
- **AC-6.1.3:** Health check endpoint returns 200 status
- **AC-6.1.4:** System handles all three test SKUs correctly

### 6.2 SKU-Specific Validation

**SKU-A (Stockout Case):**
- **AC-6.2.1:** Pricing recommends INCREASE
- **AC-6.2.2:** Forecast shows STOCKOUT_RISK
- **AC-6.2.3:** Copilot recommends DO_NOT_DISCOUNT
- **AC-6.2.4:** All phases agree on stockout scenario

**SKU-B (Dead Stock Case):**
- **AC-6.2.5:** Pricing recommends STRONG_DISCOUNT
- **AC-6.2.6:** Forecast shows DEAD_STOCK_RISK
- **AC-6.2.7:** Copilot recommends STRONG_DISCOUNT
- **AC-6.2.8:** All phases agree on dead stock scenario

**SKU-C (Overstock Case):**
- **AC-6.2.9:** Pricing recommends DISCOUNT
- **AC-6.2.10:** Forecast shows OVERSTOCK_RISK
- **AC-6.2.11:** Copilot recommends MILD_DISCOUNT
- **AC-6.2.12:** All phases agree on overstock scenario

### 6.3 Data Integrity

- **AC-6.3.1:** Pricing output changes when inventory changes
- **AC-6.3.2:** Pricing output changes when sales data changes
- **AC-6.3.3:** No hardcoded SKU-specific logic exists
- **AC-6.3.4:** All decisions are data-driven

---

## 7. Future Enhancements

### 7.1 Planned Features

- **FE-7.1.1:** Live marketplace price ingestion
- **FE-7.1.2:** Multi-store SKU analysis
- **FE-7.1.3:** Frontend dashboard for sellers
- **FE-7.1.4:** Real-time trend integration
- **FE-7.1.5:** Machine learning-based forecasting
- **FE-7.1.6:** Historical decision tracking
- **FE-7.1.7:** A/B testing framework for pricing strategies

---

## Document Version

- **Version:** 1.0
- **Last Updated:** 2025-02-09
- **Status:** Active
