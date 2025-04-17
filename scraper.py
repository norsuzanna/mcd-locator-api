from playwright.async_api import async_playwright
import re

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
                name_el = await store.query_selector(".addressTitle")
                name = await name_el.inner_text() if name_el else "No Name"

                address_el = await store.query_selector(".addressText")
                address = await address_el.inner_text() if address_el else "No Address"

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

                # Append the store data to the result
                data.append({
                    "name": name.strip(),
                    "address": address.strip(),
                    "operating_hours": '6.30 AM to 12 AM',
                    "latitude": lat,
                    "longitude": lng,
                    "waze_link": waze_link
                })

            except Exception as e:
                print(f"Error processing store: {e}")
                continue

        await browser.close()
        return data
