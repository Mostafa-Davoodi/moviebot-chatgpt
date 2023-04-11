import logging
import openai
import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

API_TOKEN = os.environ["TELEGRAM_API_TOKEN"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

openai.api_key = OPENAI_API_KEY
logging.basicConfig(level=logging.INFO)


def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        'Hello! Send me a message to get movie recommendations.')


def get_movie_recommendation(update: Update, context: CallbackContext):
    user_query = update.message.text
    prompt = f"Recommend a movie based on the following: {user_query}"

    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.8,
    )

    movie_recommendation = response.choices[0].text.strip()
    update.message.reply_text(movie_recommendation)


def main():
    updater = Updater(API_TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command, get_movie_recommendation))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
