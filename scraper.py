from playwright.async_api import async_playwright
import re
from db import save_to_supabase
import json

async def scrape_mcd_kuala_lumpur():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto("https://www.mcdonalds.com.my/locate-us", timeout=60000)

        # Select Kuala Lumpur from the dropdown
        await page.select_option("#states", label="Kuala Lumpur")
        await page.click("#search-now")

        # Wait for store results to load
        await page.wait_for_selector("#results .columns", timeout=10000)
        stores = await page.query_selector_all("#results .columns")

        data = []

        for store in stores:
            try:
                # Extract ld+json script block
                json_script = await store.query_selector("script[type='application/ld+json']")
                json_text = await json_script.inner_text() if json_script else None
                details = json.loads(json_text) if json_text else {}

                name = details.get("name", "No Name")
                address = details.get("address", "No Address")
                telephone = details.get("telephone")
                latitude = details.get("geo", {}).get("latitude")
                longitude = details.get("geo", {}).get("longitude")

                # Ensure the address contains "Kuala Lumpur"
                if "Kuala Lumpur" not in address:
                    continue

                # Initialize variables for Waze link and coordinates
                waze_link = None
                lat, lng = None, None

                # Look for the Waze link in the store's <a> tag
                map_links = await store.query_selector_all("a.map_link_color")
                for link in map_links:
                    text = await link.inner_text()
                    if "Waze" in text:
                        # Click the Waze link and capture the resulting page
                        async with context.expect_page() as popup_info:
                            await link.click()

                        popup = await popup_info.value
                        waze_url = popup.url

                        # Extract latitude and longitude from Waze URL using regex
                        match = re.search(r'to=ll\.([-.\d]+)%2C([-.\d]+)', waze_url)
                        if match:
                            lat, lng = match.group(1), match.group(2)
                            waze_link = waze_url

                        await popup.close()

                 # Detect features by icon src
                feature_icons = await store.query_selector_all("img")
                icon_srcs = [await img.get_attribute("src") for img in feature_icons if await img.get_attribute("src")]

                def has_icon(keyword):
                    return any(keyword.lower() in src.lower() for src in icon_srcs)

                operating_hours = "6:30 AM to 12:00 AM"  # default
                if has_icon("ic_24h"):
                    operating_hours = "24 Hours"

                data.append({
                    "name": name.strip(),
                    "address": address.strip(),
                    "telephone": telephone,
                    "latitude": latitude,
                    "longitude": longitude,
                    "waze_link": waze_link,
                    "has_birthday_party": has_icon("ic_birthday_party"),
                    "has_breakfast": has_icon("ic_breakfast"),
                    "has_cashless_facility": has_icon("ic_cashless"),
                    "has_dessert_center": has_icon("ic_dessert"),
                    "has_drive_thru": has_icon("ic_dt"),
                    "has_mccafe": has_icon("ic_mccafe"),
                    "has_mcdelivery": has_icon("ic_mcdelivery"),
                    "has_surau": has_icon("ic_surau"),
                    "has_wifi": has_icon("ic_wifi"),
                    "has_digital_kiosk": has_icon("ic_digital_kiosk"),
                    "has_ev_charging": has_icon("ic_ev"),
                    "operating_hours": operating_hours
                })

            except Exception as e:
                print(f"Error processing store: {e}")
                continue

        await browser.close()

        await save_to_supabase(data)
        print("[SUCCESS] Data saved to Supabase")

        return data
