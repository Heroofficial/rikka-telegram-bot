#!/usr/bin/python
# -*- coding: utf-8 -*-
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, Job
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from modules.sonyan import sonyan_post
from random import randint
import importlib
import datetime
import logging
import yaml
import os
import re

# Load configs & create folders
with open("config.yml", "r") as f:
    config = yaml.load(f)
    key = config["keys"]["telegram_token"]
    channel = config["keys"]["channel"]
    directories = config["path"]

# Create folders for temporary files
for i in directories.values():
    if not os.path.exists(i):
        os.makedirs(i)

updater = Updater(token=key)
dp = updater.dispatcher
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# Import logo from a text file
with open("resources/logo.txt", "r", encoding="UTF-8") as logo_file:
    logo = logo_file.read()
    print(logo)

# Importing modules and handlers
def load_modules(dp, module):
    importlib.import_module("modules." + module).handler(dp)
    print(module)

# Dynamic module imports
print("Loading modules...\n")
modules_path = "modules"
modules = os.listdir(modules_path)
# These do net have handlers and are imported to other modules directly
not_to_import = ["__init__.py", "instagram_filters.py", "memegenerator.py", "utils.py"]
for module in modules:
    if module in not_to_import or module[-3:] != '.py':
        continue
    load_modules(dp, module[:-3])

# Import /help from a text file
with open("resources/help.txt", "r", encoding="UTF-8") as helpfile:
    help_text = helpfile.read()
    print("Help textfile imported")


# Start feature
def start(bot, update):
    if update.message.chat.type != "private":
        return
    with open("resources/hello.webp", "rb") as hello:
        update.message.reply_sticker(hello, quote=False)
    personname = update.message.from_user.first_name
    update.message.reply_text("Konnichiwa, " + personname + "! \nMy name is Takanashi Rikka desu! \
                              \nUse /help to see what I can do! :3", quote=False)
    print(datetime.datetime.now(), ">>>", "Done /start", ">>>", update.message.from_user.username)
dp.add_handler(CommandHandler("start", start))


# Show help
def help(bot, update):
    bot.send_message(update.message.chat_id, help_text, parse_mode="Markdown")
    print(datetime.datetime.now(), ">>>", "Done /help", ">>>", update.message.from_user.username)
dp.add_handler(CommandHandler("help", help))

# Starting bot
updater.start_polling(clean=True)
# Run the bot until you presses Ctrl+C
print("=====================\nUp and running!\n")
#Job Queue for channel posts
#jobQueue = updater.job_queue
#jobQueue.run_repeating(callback=sonyan_post, interval=60, first=0, context="@"+channel, name='RepeatingJob')
#Idle
updater.idle()
