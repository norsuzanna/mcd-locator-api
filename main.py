from fastapi import FastAPI
from scraper import scrape_mcd_kuala_lumpur
import asyncio

app = FastAPI()

@app.get("/scrape")
async def scrape_endpoint():
    stores_data = await scrape_mcd_kuala_lumpur()
    return stores_data
