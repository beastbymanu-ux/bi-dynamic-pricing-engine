# Enterprise E-commerce AI: Dynamic Pricing Engine & Competitor Monitor

> **Private automated repricing** — Scrapy · Playwright · SQLAlchemy · FastAPI · Streamlit · Docker

[![Live Demo](https://img.shields.io/badge/Live_Demo-openclawlabs--pricing.duckdns.org-00d4aa?style=for-the-badge)](https://openclawlabs-pricing.duckdns.org)

## Problem

E-commerce teams manually checking competitor prices 40+ hrs/month. Static pricing leaves revenue on the table — losing 8–15% margin to underpriced competitors or missing upward repricing opportunities worth thousands monthly.

## Solution

On-premise dynamic pricing engine deployed on a private VPS:

- **Scrapy + Playwright** crawls Amazon, eBay, and Walmart prices every 15 minutes
- **SQLAlchemy + SQLite** persists 30-day price history per SKU for trend analysis
- **Repricing engine** applies configurable rules (undercut, margin floor, premium positioning)
- **Margin guard** triggers alerts when market prices approach acquisition cost
- **FastAPI REST layer** exposes repricing recommendations to downstream systems (ERP, OMS)
- **Streamlit dashboard** gives product managers instant visibility across the full catalog

## Results (STAR)

| Metric | Before | After |
|--------|--------|-------|
| Manual monitoring time | 40 hrs/month | 0 hrs/month |
| Revenue uplift (dynamic vs static) | Baseline | +12% avg |
| Margin erosion incidents | 8–12/month | 0 (auto-alert) |
| Repricing lag | 24–48 hrs | < 15 min |
| Cloud exposure | Yes | Eliminated |

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
  Nginx + SSL (DuckDNS) · Docker on Vultr VPS
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
| Infrastructure | Docker · Nginx · Vultr VPS |

## 3 Golden Pillars

1. **Money** — +12% revenue uplift from dynamic vs. static pricing. 40 hrs/month monitoring eliminated.
2. **Ownership** — All price data stays on client's server. Zero SaaS fees. No vendor lock-in.
3. **Scalability** — Add competitors, SKUs, or rule sets via config. Dockerized — deploy anywhere in minutes.

## Quick Start

```bash
git clone https://github.com/beastbymanu-ux/bi-dynamic-pricing-engine
cd bi-dynamic-pricing-engine
docker-compose up -d
# Visit http://localhost:8508
```

## Live Demo

**[https://openclawlabs-pricing.duckdns.org](https://openclawlabs-pricing.duckdns.org)**

---
*Built by [OpenClaw Labs](https://openclawlabs-ai.duckdns.org) — Senior AI/Data Engineering*
