from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, AsyncGenerator
from supabase import create_client
import os
from openai import OpenAI
from scraper import scrape_mcd_kuala_lumpur  # optional, keep if needed

# === FastAPI app ===
app = FastAPI()

# === CORS Configuration ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://mcd-locator.vercel.app"],  # or ["*"] for dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Environment Variables ===
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# === Supabase Client ===
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# === OpenAI Client ===
client = OpenAI(api_key=OPENAI_API_KEY)

# === Pydantic Model ===
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

# === Scraper Endpoint (optional) ===
@app.get("/scrape")
async def scrape_endpoint():
    stores_data = await scrape_mcd_kuala_lumpur()
    return stores_data

# === Outlet Listing ===
@app.get("/outlets", response_model=List[Outlet])
async def list_outlets():
    response = supabase.table("outlets").select("*").execute()
    outlets_data = response.data
    outlets = [Outlet(**outlet) for outlet in outlets_data]
    return outlets

# === Chat Endpoint with Streaming ===
@app.post("/chat")
async def chat_endpoint(request: Request):
    body = await request.json()
    user_message = body.get("message", "")

    async def chat_stream() -> AsyncGenerator[str, None]:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant for McDonald's Malaysia outlet locator. You can answer questions about outlet features, location, services, and nearby landmarks.",
                },
                {"role": "user", "content": user_message},
            ],
            stream=True,
        )

        for chunk in response:
            delta = chunk.choices[0].delta
            if hasattr(delta, "content") and delta.content:
                yield f"data: {delta.content}\n"

        yield "data: [DONE]\n"

    return StreamingResponse(chat_stream(), media_type="text/event-stream")
