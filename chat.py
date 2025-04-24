from fastapi import Request
from fastapi.responses import StreamingResponse
from models import Outlet
from supabase import create_client
import os
from typing import List

# Define the connection to Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

async def chatbox(request: Request):
    body = await request.json()
    user_message = body.get("message", "")
    
    # Get all outlets from Supabase
    response = supabase.table("outlets").select("*").execute()
    outlets_data = response.data
    outlets = [Outlet(**outlet) for outlet in outlets_data]
    
    async def chat_stream():
        # Process the user message and generate a reply
        reply = handle_chat(user_message, outlets)
        
        # Streaming the reply to the client
        yield f"data: {reply}\n"

    # Returning the stream as a response
    return StreamingResponse(chat_stream(), media_type="text/event-stream")

def handle_chat(user_message: str, outlets: List[Outlet]) -> str:
    """
    Handle the chat logic based on the user's query.
    This function matches common queries to outlet properties and returns an appropriate response.
    """
    user_message = user_message.lower()

    # Define helper functions to match various types of queries
    def is_open_24_hours(outlet: Outlet) -> bool:
        """Check if the outlet is open 24 hours."""
        return '24 hours' in outlet.operating_hours.lower()

    def find_outlets_by_feature(outlet: Outlet, feature: str) -> bool:
        """Check if an outlet has a specific feature."""
        features = {
            "wifi": outlet.has_wifi,
            "mccafe": outlet.has_mccafe,
            "mcdelivery": outlet.has_mcdelivery,
            "birthday party": outlet.has_birthday_party,
            "breakfast": outlet.has_breakfast,
            "cashless": outlet.has_cashless_facility,
            "digital kiosk": outlet.has_digital_kiosk,
            "ev charging": outlet.has_ev_charging
        }
        return features.get(feature, False)

    # Check for common queries and return the corresponding response
    if "24 hours" in user_message:
        open_24_hours_outlets = [outlet.name for outlet in outlets if is_open_24_hours(outlet)]
        if open_24_hours_outlets:
            return "Here are the outlets that are open 24 hours:\n" + "\n".join(open_24_hours_outlets)
        else:
            return "Sorry, no outlets are open 24 hours."

    elif any(feature in user_message for feature in ["wifi", "mccafe", "mcdelivery", "birthday party", "breakfast", "cashless", "digital kiosk", "ev charging"]):
        feature = next(feature for feature in ["wifi", "mccafe", "mcdelivery", "birthday party", "breakfast", "cashless", "digital kiosk", "ev charging"] if feature in user_message)
        matching_outlets = [outlet.name for outlet in outlets if find_outlets_by_feature(outlet, feature)]
        
        if matching_outlets:
            return f"Here are the outlets with {feature}:\n" + "\n".join(matching_outlets)
        else:
            return f"Sorry, no outlets found with {feature}."

    elif "mcd" in user_message or "mcdonald's" in user_message:
        # For general inquiries
        return "Please ask about specific outlet features like 24 hours, Wi-Fi, McCafé, etc."

    return "I'm sorry, I didn't understand that. Please ask about McDonald's outlets."
