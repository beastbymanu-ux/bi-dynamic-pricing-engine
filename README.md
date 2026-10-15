# Enterprise E-commerce AI: Dynamic Pricing Engine & Competitor Monitor

> Own project by Manu (OpenClaw Labs), built and tested with demo data. Not a client deployment.

> **Private automated repricing** — Scrapy · Playwright · SQLAlchemy · FastAPI · Streamlit · Docker

## Problem

E-commerce teams manually checking competitor prices 40+ hrs/month. Static pricing leaves revenue on the table — losing 8–15% margin to underpriced competitors or missing upward repricing opportunities worth thousands monthly.

## Solution

On-premise dynamic pricing engine designed to run on a private VPS:

- **Scrapy + Playwright** crawls Amazon, eBay, and Walmart prices every 15 minutes
- **SQLAlchemy + SQLite** persists 30-day price history per SKU for trend analysis
- **Repricing engine** applies configurable rules (undercut, margin floor, premium positioning)
- **Margin guard** triggers alerts when market prices approach acquisition cost
- **FastAPI REST layer** exposes repricing recommendations to downstream systems (ERP, OMS)
- **Streamlit dashboard** gives product managers instant visibility across the full catalog

## Architecture

```
Amazon · eBay · Walmart
        │
  Scrapy Spiders + Playwright (JS-rendered fallback)
        │
  SQLAlchemy ORM → SQLite (on-premise, 30-day history)
        │
  Repricing Engine (5 configurable rules)
        │
  FastAPI REST  ←→  Streamlit Dashboard
        │
```

## Repricing Rules

| Rule | Logic |
|------|-------|
| Undercut Lowest | Always 1% below cheapest competitor |
| Fixed Margin 15% | Price floor = cost × 1.15 |
| Aggressive -3% | 3% below lowest (volume strategy) |
| Premium +5% | 5% above market avg (brand positioning) |
| Beat Amazon Only | Match Amazon -0.5% only when Amazon is cheapest |

## Stack

| Component | Technology |
|-----------|-----------|
| Web Scraping | Scrapy + Playwright |
| ORM / Persistence | SQLAlchemy + SQLite |
| API Layer | FastAPI |
| Dashboard | Streamlit + Plotly |
| Infrastructure | Docker · Nginx · private VPS |

## Design principles

1. **Ownership** — All price data stays on your own server. Zero SaaS fees. No vendor lock-in.
2. **Scalability** — Add competitors, SKUs, or rule sets via config. Dockerized — deploy anywhere in minutes.

## Quick Start

```bash
git clone https://github.com/beastbymanu-ux/bi-dynamic-pricing-engine
cd bi-dynamic-pricing-engine
docker-compose up -d
# Visit http://localhost:8508
```
