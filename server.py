from math import prod
from urllib import response
import requests
from bs4 import BeautifulSoup
import time
import os

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"}

watchlist = []


def main(url):
    try:
        # print("In main")
        response = requests.get(url, headers=headers)
        print(response.status_code)
        page = response.text
        soup = BeautifulSoup(page, "lxml")

        title = soup.find(id="productTitle").text.strip()
        price = float(soup.find(
            "span", "priceToPay").span.text.strip()[1:])

        for product in watchlist:
            if product["title"] == title:
                return 1

        watchlist.append({"title": title, "price": price, "url": url})
        while True:
            print("While loop is executing...")
            print(os.getpid())
            for product in watchlist:
                page = requests.get(product["url"], headers=headers).text
                soup = BeautifulSoup(page, "lxml")

                title = soup.find(id="productTitle").text.strip()
                current_price = float(soup.find(
                    "span", "priceToPay").span.text.strip()[1:])

                if current_price < product["price"]:
                    product["price"] = current_price
                    return product
                time.sleep(30)
        print("I'm out")
        print(watchlist)
        # print(title)
        # print(price)

    except requests.HTTPError:
        print("An http error occured.")
        pass


if __name__ == "__main__":
    url = "https://www.amazon.in/Dell-KB216-Wired-Multimedia-Keyboard/dp/B00ZYLMQH0/ref=sr_1_3?crid=X0A00ZWYCCS9&keywords=keyboard&qid=1659940584&sprefix=keyboar%2Caps%2C271&sr=8-3"
    main(url)
