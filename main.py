from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from supabase import create_client
from pydantic import BaseModel
from typing import List, AsyncGenerator
from openai import AsyncOpenAI
import os

from scraper import scrape_mcd_kuala_lumpur  # Your scraper module

app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://mcd-locator.vercel.app/"],  # Replace with specific origin(s) in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize clients
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
client = AsyncOpenAI(api_key=OPENAI_API_KEY)


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
    Retrieves all outlets from Supabase.
    """
    response = supabase.table("outlets").select("*").execute()
    outlets_data = response.data
    return [Outlet(**outlet) for outlet in outlets_data]


@app.post("/chat")
async def chat_endpoint(request: Request):
    body = await request.json()
    user_message = body.get("message", "")

    async def chat_stream() -> AsyncGenerator[str, None]:
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant for McDonald's Malaysia outlet locator. You can answer questions about outlet features, locations, and services.",
                },
                {"role": "user", "content": user_message},
            ],
            stream=True,
        )

        async for chunk in response:
            delta = chunk.choices[0].delta
            if hasattr(delta, "content") and delta.content:
                yield f"data: {delta.content}\n"

        yield "data: [DONE]\n"

    return StreamingResponse(chat_stream(), media_type="text/event-stream")
