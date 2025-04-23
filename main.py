from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from supabase import create_client
from openai import AsyncOpenAI
from pydantic import BaseModel
from typing import List, AsyncGenerator
import os
import asyncio

# Load environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# CORS config
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://mcd-locator.vercel.app"],  # Replace with your frontend URL in production
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
    body = await request.json()
    user_message = body.get("message", "")

    # Function to check if an outlet operates 24 hours
    def is_open_24_hours(outlet):
        # Check if operating_hours contains '24 hours' (case-insensitive)
        return '24 hours' in outlet.operating_hours.lower()

    # Fetch all outlets from Supabase
    response = supabase.table("outlets").select("*").execute()
    outlets_data = response.data
    outlets = [Outlet(**outlet) for outlet in outlets_data]

    # If the query is asking about 24-hour outlets
    if "24 hours" in user_message.lower():
        open_24_hours_outlets = [outlet for outlet in outlets if is_open_24_hours(outlet)]
        if open_24_hours_outlets:
            response_message = "Here are the outlets that are open 24 hours:\n"
            response_message += "\n".join([outlet.name for outlet in open_24_hours_outlets])
        else:
            response_message = "Sorry, no outlets are open 24 hours."
    else:
        response_message = "I'm sorry, I didn't understand that. Please ask about McDonald's outlets."

    # Stream the response
    async def chat_stream():
        yield f"data: {response_message}\n"
        yield "data: [DONE]\n"

    return StreamingResponse(chat_stream(), media_type="text/event-stream")

