from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from supabase import create_client
from openai import AsyncOpenAI
from pydantic import BaseModel
from typing import List, AsyncGenerator
import os
import asyncio
from scraper import scrape_mcd_kuala_lumpur
from chat import chatbox

# Load environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# CORS config
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://mcd-locator.vercel.app", "https://r5f943-3000.csb.app"],  # Replace with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# OpenAI client
client = AsyncOpenAI(api_key=OPENAI_API_KEY)

# Outlet schema
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
    Get all outlets from Supabase.
    """
    response = supabase.table("outlets").select("*").execute()
    outlets_data = response.data
    return [Outlet(**outlet) for outlet in outlets_data]

@app.post("/chat")
async def chat_endpoint(request: Request):
    return await chatbox(request)