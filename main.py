from flask import Flask
import threading, time, requests, os

app = Flask(__name__)

# Discord-webhook från miljövariabel
WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

SEARCH_QUERY = "ralph lauren polo"
MAX_PRICE = 150
SLEEP_INTERVAL = 600 # 10 minuter

def send_to_discord(title, price, url, image):
    """Skicka meddelande till Discord via webhook"""
    data = {
        "content": f"👕 **{title}**\n💰 {price} kr\n🔗 {url}",
        "embeds": [{"image": {"url": image}}] if image else []
    }
    try:
        requests.post(WEBHOOK_URL, json=data)
    except:
        pass

def search_vinted_loop():
    """Kontinuerlig sökning på Vinted"""
    while True:
        url = f"https://www.vinted.se/api/v2/catalog/items?search_text={SEARCH_QUERY}&price_to={MAX_PRICE}"
        try:
            res = requests.get(url)
            items = res.json().get("items", [])
            for item in items:
                title = item.get("title", "okänd produkt")
                price = item.get("price", "okänt pris")
                link = f"https://www.vinted.se/items/{item.get('id')}"
                image = item.get("photo", {}).get("url", "")
                send_to_discord(title, price, link, image)
        except:
            pass
        time.sleep(SLEEP_INTERVAL)

# Starta Vinted-loopen i en separat tråd
threading.Thread(target=search_vinted_loop, daemon=True).start()

@app.route("/")
def home():
    return "Bot running!"

if __name__ == "__main__":
    # Render skickar port via miljövariabeln PORT
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
