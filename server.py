import requests
from bs4 import BeautifulSoup
import time
import os


# User agent headers

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
}

# Array to store the items being monitored

watchlist = []

# Main function


def main(url):
    try:
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
                        return product

                    # If priceraise then update the price of item in watchlist

                    elif current_price > product["price"]:
                        product["price"] = current_price

                    # Sleep for 10 mins
                    print(watchlist)
                    print("Sleeping..")
                    time.sleep(10)
        else:
            print("They probably blocked you")
            pass
    except requests.HTTPError:
        print("An http error occured.")
    except TimeoutError:
        print("Connection timed out")


if __name__ == "__main__":
    url = "http://127.0.0.1:5500/amazon.html"
    main(url)
