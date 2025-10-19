import requests
import time

WEBHOOK_URL = https://discord.com/api/webhooks/1429129495524151349/-lRyNg2rHM-Q4qRbTIm8H-Pja2fLs3HoL6Lf-L7Y5bK_Ch_-dLsgc3pH8P4f_jVJdobw
SEARCH_QUERY = "ralph lauren polo"
MAX_PRICE = 150

def send_to_discord(title, price, url, image):
    data = {
        "content": f"👕 **{title}**\n💰 {price} kr\n🔗 {url}",
        "embeds": [{"image": {"url": image}}],
    }
    requests.post(WEBHOOK_URL, json=data)

def search_vinted():
    url = f"https://www.vinted.se/api/v2/catalog/items?search_text={SEARCH_QUERY}&price_to={MAX_PRICE}"
    res = requests.get(url)
    if res.status_code == 200:
        items = res.json().get("items", [])
        for item in items:
            title = item.get("title", "okänd produkt")
            price = item.get("price", "okänt pris")
            link = f"https://www.vinted.se/items/{item.get('id')}"
            image = item.get("photo", {}).get("url", "")
            send_to_discord(title, price, link, image)

while True:
    search_vinted()
    time.sleep(600)
