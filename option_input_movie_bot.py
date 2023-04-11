import logging
import openai
import os
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext,
    CallbackQueryHandler,
)

API_TOKEN = os.environ["TELEGRAM_API_TOKEN"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

openai.api_key = OPENAI_API_KEY
logging.basicConfig(level=logging.INFO)


def start(update: Update, context: CallbackContext):
    intro_message = (
        "🎬 Welcome to the MovieBot! 🎬\n\n"
        "I can help you discover the top 5 movies in different categories. "
        "Please choose a movie category from the options below:"
    )

    keyboard = [
        [
            InlineKeyboardButton("🎭 Drama", callback_data="drama"),
            InlineKeyboardButton("🎬 Action", callback_data="action"),
            InlineKeyboardButton("🔮 Sci-fi", callback_data="sci-fi"),
        ],
        [
            InlineKeyboardButton("👻 Horror", callback_data="horror"),
            InlineKeyboardButton("😂 Comedy", callback_data="comedy"),
            InlineKeyboardButton("💘 Romance", callback_data="romance"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(intro_message, reply_markup=reply_markup)


def get_movie_recommendation(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    movie_category = query.data
    prompt = f"Give me the list of 5 top movies in the {movie_category} category"

    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.8,
    )

    movie_recommendation = response.choices[0].text.strip()
    query.edit_message_text(movie_recommendation)


def main():
    updater = Updater(API_TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(get_movie_recommendation))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
