from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_DB_CONFIG = {
    "url": os.getenv("SUPABASE_URL"),
    "key": os.getenv("SUPABASE_KEY"),
    "table": "outlets"
}

url = SUPABASE_DB_CONFIG["url"]
key = SUPABASE_DB_CONFIG["key"]
table_name = SUPABASE_DB_CONFIG["table"]

supabase = create_client(url, key)

async def save_to_supabase(data: list[dict]):
    for item in data:
        try:
            supabase.table(table_name).insert(item).execute()
        except Exception as e:
            print(f"[ERROR] Failed to insert {item['name']}: {e}")
