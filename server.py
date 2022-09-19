from itertools import product
import requests
from bs4 import BeautifulSoup
import time
import os
import telebot
import json

# from bot import watchlist

# User agent headers

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
}

# Initalizing bot object with the API_KEY

bot = telebot.TeleBot(os.getenv("API_KEY"))

# Scrapper function


def scrapper(url):
    try:
        if os.path.getsize("watchlist.json") > 0:
            with open("watchlist.json") as f:
                watchlist = json.load(f)
        else:
            watchlist = []

        # Make get request to the url
        response = requests.get(url, headers=headers, timeout=2)
        page = response.text

        # Scrape the page
        soup = BeautifulSoup(page, "lxml")
        title = soup.find(id="productTitle")
        price = soup.find(
            "span", "priceToPay")

        if title and price:
            title = title.text.strip()
            price = float(price.span.text.strip().replace(",", "")[1:])

            # Append the item to the watch list
            watchlist.append({"title": title, "price": price, "url": url})

            with open("watchlist.json", "w") as f:
                print("Written item into file")
                f.write(json.dumps(watchlist))

            watcher(watchlist)

        else:
            print("They probably blocked you")
            pass
    except requests.HTTPError:
        print("An http error occured.")
    except TimeoutError:
        print("Connection timed out")


# Watcher function
def watcher(watchlist):
    # Keep checking for price drops for all items in watchlist
    while True:
        for product in watchlist:
            page = requests.get(product["url"], headers=headers).text
            soup = BeautifulSoup(page, "lxml")

            title = soup.find(id="productTitle").text.strip()
            current_price = float(soup.find(
                "span", "priceToPay").span.text.strip().replace(",", "")[1:])

            # If pricedrop found alert user

            if current_price < product["price"]:
                product["price"] = current_price
                alert_user(product)

            # If priceraise then update the price of item in watchlist

            elif current_price > product["price"]:
                product["price"] = current_price

            # Sleep for 10 mins
            print(watchlist)
            print("Sleeping..")
            time.sleep(10)


def alert_user(product):
    updates = bot.get_updates()
    bot.send_message(
        updates.message.chat.id, f"The price is drippin for {product['title']}")


if __name__ == "__main__":
    url = "http://127.0.0.1:5500/amazon.html"
    watcher(url)
