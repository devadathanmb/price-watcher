import telebot
from dotenv import load_dotenv
import os
import validators
import requests
from quoters import Quote
import json
from multiprocessing import Process
from watcher import watcher
from watcher import scrapper

# Load environemnt variables from .env

load_dotenv()

# Initalizing bot object with API_KEY

bot = telebot.TeleBot(os.getenv("API_KEY"))

# User agent headers

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36"}

# Inital config

watching = False
watch_process = None

# Handle start command


@bot.message_handler(commands=["start"])
def start(message):
    reply = '''
    Welcome to price watcher. I can watch the price drops for you. Send /help to see how to use me.
    '''
    bot.reply_to(message, reply)


# Handle help command

@bot.message_handler(commands=["help"])
def send_hello(message):
    reply_message = f'''Available commands:
/watch <Amazon url here> - To watch the price of the item
/watchlist - To display the items currently being monitored
/dontwatch <watch id> - To remove the item from watch list
/clearlist - To clear the watch list
/help - To display available commands
'''
    bot.send_message(message.chat.id, reply_message)


# Handle watch command

@bot.message_handler(commands=["watch"])
def watch(message):
    print("In watch")

    splitted_message = message.text.partition("/watch")
    link = splitted_message[2].strip()

    # Create watchlist.json if it does not exist
    if not os.path.exists("watchlist.json"):
        with open("watchlist.json", "w") as file:
            pass

    # Load or initalize watchlist
    if not is_empty("watchlist.json"):
        with open("watchlist.json", "r") as file:
            watchlist = json.load(file)
    else:
        watchlist = []

    # If URL not given
    if len(link) == 0:
        bot.reply_to(message, "Please provide the link")

    # If URL not valid
    elif not validators.url(link):
        bot.reply_to(
            message, "Oops.. That does not seem like a valid link. Try again.")

    # If not amazon URL
    elif "amazon" in link:
        try:
            # Check if amazon url is valid
            response = requests.get(link, headers=headers)
            if response.status_code == 200:
                # Check if the product is already present in the watchlist
                already_watching = False
                for product in watchlist:
                    if product["url"] == link:
                        already_watching = True
                        bot.reply_to(message, "I'm already watching it.")
                        return
                if not already_watching:
                    bot.reply_to(message, "Alright.. I got my eyes on you!")

                # Create a new process to watch the prices
                global watching
                global watch_process

                # If already watching the list, then terminate it
                if watching:
                    watch_process.terminate()

                # Starting the new process
                watch_process = Process(
                    target=scrapper, args=(link, message.chat.id))
                watch_process.start()
                watching = True

            else:
                response.raise_for_status()
        except ConnectionError:
            bot.reply_to(
                message, "Something is not working.. Try again later.")

        except TimeoutError:
            bot.reply_to(
                message, "Something is not working.. Try again later.")

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                bot.reply_to(message, "Are you sure that link is correct?")
            else:
                bot.reply_to(message, "Oops.. Something went wrong.")
    else:
        bot.reply_to(
            message, "I only work with amazon links for now.")

# Handle watchlist command


@bot.message_handler(commands=["watchlist"])
def handle_watchlist(message):
    if not is_empty("watchlist.json"):
        with open("watchlist.json") as f:
            watchlist = json.load(f)
    else:
        watchlist = []
    if len(watchlist) == 0:
        bot.reply_to(message, "There is nothing in the watchlist.")
    else:
        reply = ""
        for index, product in enumerate(watchlist):
            reply += str(index + 1) + ". " + product["title"] + "\n"
        bot.reply_to(message, reply)


# Handle clear watchlist command

@bot.message_handler(commands=["clearlist"])
def clearlist(message):
    if not is_empty("watchlist.json"):
        with open("watchlist.json", "w") as file:
            file.truncate(0)
            try:
                watch_process.terminate()
            except AttributeError:
                pass
            bot.reply_to(message, "The watchlist has been cleared.")
    else:
        bot.reply_to(message, "The watchlist is already empty")

# Handle dontwatch command


@bot.message_handler(commands=["dontwatch"])
def dontwatch(message):
    splitted_message = message.text.partition("/dontwatch")
    index = splitted_message[2]
    if len(index) == 0:
        bot.reply_to(
            message, "Please provide what product to remove from the watchlist.")
    else:
        try:
            index = int(index)

            with open("watchlist.json", "r") as file:
                watchlist = json.load(file)
            bot.reply_to(
                message, f"Not watching {watchlist[index - 1]['title']} anymore")
            watchlist.pop(index - 1)
            print("Removing the item, terminating old process and starting new process")
            global watch_process
            try:
                watch_process.terminate()
            except AttributeError:
                pass
            with open("watchlist.json", "w") as file:
                file.write(json.dumps(watchlist))
            watch_process = Process(
                target=watcher, args=(watchlist, message.chat.id))
            if len(watchlist) > 0:
                watch_process.start()
        except ValueError:
            bot.reply_to(message, "That does not seem like a valid number.")
        except IndexError:
            bot.reply_to(message, "There is no product in that index.")


# Handle random message

@bot.message_handler()
def random_message(message):
    bot.reply_to(message, Quote.print())
    bot.send_message(message.chat.id, "/help for help")


# Function to check if the json file is empty
def is_empty(jsonfile):
    if os.path.getsize(jsonfile) == 0:
        return True
    else:
        with open(jsonfile, "r") as file:
            watchlist = json.load(file)
            if len(watchlist) == 0:
                return True
            else:
                return False


# Bot is active
print("Bot is up and running.")
bot.infinity_polling()
