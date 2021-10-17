"""
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
from typing import Dict

from telegram import ReplyKeyboardMarkup, Update, ReplyKeyboardRemove
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)
# user-defined functions and constants
from data_handler import Data_handler
from constants import BOT_TOKEN, DB_PATH # нужно сюда поставить токен бота и путь к файлу с БД


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

CHOOSING, TYPING_VAL, TYPING_PARAM = range(3)

start_keyboard = [
    ['Fetch data', 'Insert data'],
    ['Done'],
]
start_markup = ReplyKeyboardMarkup(start_keyboard, one_time_keyboard=True)

body_keyboard = [
    ['Proceed with a new param'],
    ['Done'],
]
body_markup = ReplyKeyboardMarkup(body_keyboard, one_time_keyboard=True)

# Add a custom db wrapper
db = Data_handler(DB_PATH)

def udata_to_str(user_data: Dict[str, str]) -> str:
    """Helper function for formatting the gathered user info."""
    facts = [f'{key} : {value}' for key, value in user_data.items()]
    return "\n".join(facts).join(['\n', '\n'])


def start(update: Update, context: CallbackContext) -> int:
    """Start the conversation and ask user to choose an action."""
    update.message.reply_text(
        "Hi! Homer bot is here, duh.\n"
        "I can fetch you deal price based on params you provide or update the database with your data.\n"
        "What do you want?",
        reply_markup=start_markup,
    )
    context.user_data['param_dict'] = {}

    return CHOOSING

def initiate_fetch(update: Update, context: CallbackContext) -> int:
    """Invite user to provide an *independent param*."""
    update.message.reply_text(
    "Alright, please send me the name of the parameter first:")
    context.user_data['action'] = 'Fetch'

    return TYPING_PARAM


def get_param_name(update: Update, context: CallbackContext) -> int:
    """Ask the user for a name of the *independent param*."""
    text = update.message.text
    context.user_data['choice'] = text
    # place to hold user data input 
    update.message.reply_text(f'Your param is {text.lower()}? Please, provide its value.')

    return TYPING_VAL


def get_param_val(update: Update, context: CallbackContext) -> int:
    """Store info provided by user and ask for the next param if needed."""
    user_data = context.user_data
    text = update.message.text
    param_name = user_data['choice']
    user_data['param_dict'][param_name] = text
    del user_data['choice']

    # TODO delete this print after debug
    print(user_data)
    
    if context.user_data['action'] == 'Fetch':
        try:
            result_dict = db.get_param(user_data['param_dict'])
        except KeyError:
            update.message.reply_text(
                "Neat! Just so you know, below are the params and vals you entered:"
                f"{udata_to_str(user_data['param_dict'])}\n"
                "No such parameter in db."
                ,
                reply_markup=body_markup,
            )
            # delete wrong entry from the user_data
            del user_data['param_dict'][param_name]

            return CHOOSING

        # TODO delete this print after debug
        print(user_data)
        
        try:
            avg_param = sum(result_dict.values())/len(result_dict)
        except ZeroDivisionError:
            avg_param = 'NULL'

        update.message.reply_text(
            "Neat! Just so you know, below are the params and vals you entered:"
            f"{udata_to_str(user_data['param_dict'])}"
            f"There are {len(result_dict)} lines matching params provided."
            f"Corresponding average price is {avg_param}.\n"
            "You can tell me more, or change the nature of interaction."
            ,
            reply_markup=body_markup,
        )

        if len(result_dict) <= 17:
            update.message.reply_text(
                "Below are the ids matching the pattern:"
                f"{udata_to_str(result_dict)}"
            )

        return CHOOSING

    # TODO add messages to user
    # TODO refactor the code into multiple sub functions
    if context.user_data['action'] == 'Insert':
        try:
            db.append_entry(context.user_data['param_dict'])
        except ValueError:
            update.message.reply_text(
            "Neat! Just so you know, below are the params and vals you entered:"
            f"{udata_to_str(user_data['param_dict'])}\n"
            "db has no such column."
            ,
            reply_markup=body_markup,
        )
        return CHOOSING

def initiate_insert(update: Update, context: CallbackContext) -> int:
    """Ask the user for a description of a custom param_name."""
    update.message.reply_text(
    "Alright, please send me the name of the parameter first:")
    context.user_data['action'] = 'Insert'

    return TYPING_PARAM


def done(update: Update, context: CallbackContext) -> int:
    """Display the gathered info and end the conversation."""
    user_data = context.user_data
    if 'choice' in user_data:
        del user_data['choice']

    update.message.reply_text(
        f"Below are the data you provided: {udata_to_str(user_data['param_dict'])} Until next time!",
        reply_markup=ReplyKeyboardRemove(),
    )

    user_data.clear()
    return ConversationHandler.END

# TODO change the default text
def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(BOT_TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add conversation handler with the states CHOOSING, TYPING_PARAM and TYPING_VAL
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOOSING: [
                MessageHandler(
                    Filters.regex('^(Fetch data)$') | Filters.regex('^Proceed with a new param$'), 
                    initiate_fetch),
                MessageHandler(Filters.regex('^Insert data$'), initiate_insert),
                # MessageHandler(Filters.regex('^Proceed with a new param$'), initiate_fetch),
            ],
            TYPING_PARAM: [
                MessageHandler(Filters.text & ~(Filters.command | Filters.regex('^Done$')), get_param_name)
            ],
            TYPING_VAL: [
                MessageHandler(
                    Filters.text & ~(Filters.command | Filters.regex('^Done$')),
                    get_param_val,
                )
            ],
        },
        fallbacks=[MessageHandler(Filters.regex('^Done$'), done)],
    )

    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()