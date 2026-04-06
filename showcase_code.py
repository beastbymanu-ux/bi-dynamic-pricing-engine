"""
bi-dynamic-pricing-engine — showcase_code.py
Core pipeline: scraping, persistence, repricing logic.
"""

# 1. Scrapy spider for competitor price extraction
import scrapy

class CompetitorPriceSpider(scrapy.Spider):
    name = "competitor_prices"
    custom_settings = {"ROBOTSTXT_OBEY": True, "DOWNLOAD_DELAY": 1.5}

    def __init__(self, sku: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sku = sku
        self.start_urls = [
            f"https://www.amazon.com/s?k={sku}",
            f"https://www.ebay.com/sch/i.html?_nkw={sku}",
        ]

    def parse(self, response):
        # Extract price from structured data (JSON-LD or span selectors)
        for product in response.css("div[data-component-type=s-search-result]"):
            price_whole = product.css("span.a-price-whole::text").get()
            price_frac  = product.css("span.a-price-fraction::text").get()
            if price_whole:
                yield {
                    "sku": self.sku,
                    "source": response.url.split("/")[2],
                    "price": float(f"{price_whole.replace(',','')}.{price_frac or '00'}"),
                    "scraped_at": __import__("datetime").datetime.utcnow().isoformat(),
                }

# 2. Playwright fallback for JS-rendered pages
from playwright.async_api import async_playwright
import asyncio

async def scrape_with_playwright(url: str, price_selector: str) -> float | None:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url, timeout=15000)
        await page.wait_for_selector(price_selector, timeout=8000)
        text = await page.inner_text(price_selector)
        await browser.close()
        clean = text.strip().replace("$","").replace("€","").replace(",","")
        return float(clean) if clean else None

# 3. SQLAlchemy persistence
from sqlalchemy import create_engine, Column, Float, String, DateTime
from sqlalchemy.orm import declarative_base, Session
from datetime import datetime

Base = declarative_base()

class PriceSnapshot(Base):
    __tablename__ = "price_snapshots"
    id         = Column(String, primary_key=True)
    sku        = Column(String, index=True)
    source     = Column(String)   # amazon | ebay | walmart | ours
    price      = Column(Float)
    scraped_at = Column(DateTime, default=datetime.utcnow)

def save_snapshot(engine, sku: str, source: str, price: float):
    with Session(engine) as s:
        snap = PriceSnapshot(
            id=f"{sku}-{source}-{int(datetime.utcnow().timestamp())}",
            sku=sku, source=source, price=price
        )
        s.add(snap)
        s.commit()

# 4. Repricing engine
def compute_suggested_price(
    our_price: float, cost: float, competitor_prices: dict, rule: str
) -> tuple[float, str]:
    lowest = min(competitor_prices.values())
    avg    = sum(competitor_prices.values()) / len(competitor_prices)
    rules = {
        "undercut_lowest":  (round(lowest * 0.99, 2),   f"1% below lowest @ {lowest:.2f}"),
        "fixed_margin_15":  (max(round(cost * 1.15, 2), round(avg * 0.98, 2)), f"15% margin floor above cost {cost:.2f}"),
        "aggressive_minus3":(round(lowest * 0.97, 2),   f"3% below lowest (volume strategy)"),
        "premium_plus5":    (round(avg * 1.05, 2),       f"5% above market avg {avg:.2f}"),
    }
    suggested, reason = rules.get(rule, (our_price, "No rule matched"))
    return suggested, reason

# 5. FastAPI endpoint (served alongside Streamlit)
from fastapi import FastAPI
app_api = FastAPI()

@app_api.get("/api/reprice/{sku}")
def reprice(sku: str, rule: str = "undercut_lowest"):
    # In production: fetch live data from DB
    return {"sku": sku, "rule": rule, "suggested_price": 0.0, "reason": "demo"}
