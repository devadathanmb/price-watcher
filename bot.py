from json import load
from urllib.error import HTTPError
import telebot
from dotenv import load_dotenv
import os
import validators
import requests


load_dotenv()

bot = telebot.TeleBot(os.getenv("API_KEY"))


headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36"}

# Handle start


@bot.message_handler(commands=["start"])
def start(message):
    reply = '''
    Welcome to price watcher. I can watch the price drops for you. Send /help to see how to use me.
    '''
    bot.reply_to(message, reply)


# Handle help


@bot.message_handler(commands=["help"])
def send_hello(message):
    reply_message = f'''Available commands:
/watch <Amazon url here> - To watch the price of the item
/watchlist - To display the items currently being monitored
/dontwatch <watch id> - To remove the item from watchlist
/help - To display available commands'''
    bot.send_message(message.chat.id, reply_message)


# Handle watch
@bot.message_handler(commands=["watch"])
def watch(message):
    splitted_message = message.text.partition("/watch")
    link = splitted_message[2].strip()
    if len(link) == 0:
        bot.reply_to(message, "Please provide the link")
    elif not validators.url(link):
        bot.reply_to(
            message, "Oops.. That does not seem like a valid link. Try again.")
    if "amazon" in link:
        try:
            response = requests.get(link, headers=headers)
            if response.status_code == 200:
                bot.reply_to(message, "Alright.. I have my eyes on it.")
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


bot.infinity_polling()
