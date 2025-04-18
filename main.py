from fastapi import FastAPI
from scraper import scrape_mcd_kuala_lumpur
import asyncio
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client
import os
from pydantic import BaseModel
from typing import List

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

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Connect to Supabase
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

class Outlet(BaseModel):
    name: str
    latitude: float
    longitude: float
    address: str
    telephone: str
    waze_link: str
    has_birthday_party: bool
    has_breakfast: bool
    has_cashless_facility: bool
    has_mccafe: bool
    has_mcdelivery: bool
    has_wifi: bool
    has_digital_kiosk: bool
    has_ev_charging: bool
    operating_hours: str

@app.get("/scrape")
async def scrape_endpoint():
    stores_data = await scrape_mcd_kuala_lumpur()
    return stores_data

@app.get("/outlets", response_model=List[Outlet])
async def list_outlets():
    """
    This endpoint retrieves all outlets from the database and returns a list of all the outlets.
    """
    # Fetch all outlets from Supabase table (you can adjust it based on your actual database)
    response = supabase.table("outlets").select("*").execute()
    
    outlets_data = response.data

    # Return the list of outlets in the required format
    outlets = [Outlet(**outlet) for outlet in outlets_data]
    
    return outlets