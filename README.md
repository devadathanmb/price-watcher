# Price watcher 🧐
A basic telegram bot written in python that allows users to check for price drops for online products.

---

## Getting started
*You can host this bot wherever you want to, even on your own machine!*

To get started: 
  
1. Make sure python and pip is installed with:

```bash
python --verson # This should return the installed version of python
pip --version # This should return the installed version of pip
```
2. Clone the repository and cd into it
```bash
git clone https://github.com/devadathanmb/Price-watcher.git
cd Price-watcher
```

3. Install the required packages using
```bash
pip install -r requirements.txt
```

4. Then generate an API token in telegram using ```BotFather``` telegram bot. See [here](https://pianalytix.com/telegram-bot-api-how-to-generate-auth-token/) for detailed steps.

5. Create a ```.env``` file in the project directory and store the generated API token into it.  
*(It should be of the format ```API_TOKEN=Your API token goes here```)*

6. Start the bot using ```python bot.py```

7. Checkout the available commands to start using the bot.
---

## Available commands

The bot offers you a number of commands to manage your price watch list and add new items to the watchlist.

```
/start - To start the bot

/help - To display all the available commands

/watch url - To watch the price of an item where url is the link to the item

/watchlist - To display all the items currently being watched

/dontwatch item_no - To stop watching an item where item_no is the number as per the output of /watchlist

/clearlist - To clear the watchlist
```

**Note that the bot only works with amazon links for now. Support for others links could be added later.**

## How does this work?

This is a very simple bot made using the [pyTelegramBotAPI](https://pypi.org/project/pyTelegramBotAPI/) python module.  
Once a product has been added to the watch list, the bot uses the [requests](https://pypi.org/project/requests/) python module to get the webpage and uses [beautifulsoup](https://pypi.org/project/beautifulsoup4/) to scrape the webpage for the need information. Since there is a limit to the number of requests to be made, the bot waits for 10 seconds before making another request.  Any price drops is notified back to the user as a telegram message. All the items to be monitored along with their corresponding url, name and current price is stored in a ```watchlist.json``` file in the project directory.
