import requests
import time
import os

# Hämta Discord-webhook från miljövariabeln
WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")
if not WEBHOOK_URL:
    raise ValueError("Ingen Discord-webhook hittad. Sätt miljövariabeln DISCORD_WEBHOOK_URL.")

# Inställningar för sökning
SEARCH_QUERY = "ralph lauren polo"
MAX_PRICE = 150
SLEEP_INTERVAL = 600 # 10 minuter

def send_to_discord(title, price, url, image):
    """Skicka meddelande till Discord via webhook"""
    if not WEBHOOK_URL:
        print("Ingen webhook angiven, skippar meddelande.")
        return
    data = {
        "content": f"👕 **{title}**\n💰 {price} kr\n🔗 {url}",
        "embeds": [{"image": {"url": image}}] if image else []
    }
    try:
        response = requests.post(WEBHOOK_URL, json=data)
        if response.status_code != 204 and response.status_code != 200:
            print("Discord-webhook returnerade fel:", response.status_code, response.text)
    except Exception as e:
        print("Kunde inte skicka till Discord:", e)

def search_vinted():
    """Sök på Vinted och skicka nya resultat till Discord"""
    url = f"https://www.vinted.se/api/v2/catalog/items?search_text={SEARCH_QUERY}&price_to={MAX_PRICE}"
    try:
        res = requests.get(url)
        res.raise_for_status()
        items = res.json().get("items", [])
        for item in items:
            title = item.get("title", "okänd produkt")
            price = item.get("price", "okänt pris")
            link = f"https://www.vinted.se/items/{item.get('id')}"
            image = item.get("photo", {}).get("url", "")
            send_to_discord(title, price, link, image)
    except Exception as e:
        print("Fel vid Vinted-sökning:", e)

if __name__ == "__main__":
    print("Vinted-notifier startar...")
    while True:
        search_vinted()
        time.sleep(SLEEP_INTERVAL)
