from fastapi import FastAPI
from scraper import scrape_mcd_kuala_lumpur
import asyncio
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://mcd-locator.vercel.app",
        "https://r5f943-3000.csb.app"
        ],  # Replace "*" with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/scrape")
async def scrape_endpoint():
    stores_data = await scrape_mcd_kuala_lumpur()
    return stores_data
