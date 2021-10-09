# general bot-related import
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, commandhandler

# user-defined functios and database management
import constants
import bot_funcs as funcs
import data_handler


import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)


print('Bot starterd...')

def start_command(update, context):
    # context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")
    update.message.reply_text("I'm a real estate analyzing bot. Use /help to find out what I can do for you.")

def help_command(update, context):
    # использую логику не из офф. источника, а: 
    # https://www.youtube.com/watch?v=PTAkiukJK7E
    # говорит, что контекст можно уже не предоставлять.
    update.message.reply_text("""
    I can do 2 things: 
    1. Given a certain parameter or set of parameters, return the corresponding price of a real estate in Moscow.
    Type /get_price *parameter* to use this option and follow the instructions. 
    2. Make a new entry into the database.
    Type /insert_entry to use this option and follow the instructions.
    """)

def get_price_command(update, context):
    """
    when called, the function prints a list of params available for fetching.
    a user is then expected to provide param name and value in two consecutive messages. 
    """
    pass

    # TODO think about relating message input to the command handler as in BotFather
    # Start a conversation consecutively asking user for param and value 
    update.message.reply_text(
    """
    Please provide one of the following params to get the corresponding price: 
    {data_handler.param_list} 
    """)

def insert_entry_command(update, context):
    
    update.message.reply_text(
    """
    when called, the function prints a list of params required to be filled in order to put a new entry in DB.
    a conversation with the user is then started in order to specify the param values 
    """)
    pass
    # TODO consecutively parse param names and values from user 

def handle_message(update, context):
    text = update.message.text
    # this is the place to decide whether the update is related to the get_price or insert_entry commands
    response = funcs.sample_responses(text)
    update.message.reply_text(response)

def error(update, context):
    print(f"Update {update} caused error {context.error}")

def main():
    updater = Updater(token=constants.BOT_TOKEN)
    # initialize dispatcher
    dp = updater.dispatcher

    # add general commands handler to the dispatcher
    dp.add_handler(CommandHandler('start', start_command))
    dp.add_handler(CommandHandler('help', help_command))
    
    # add specific commands hanlder to the dispatcher
    dp.add_handler(CommandHandler('get_price', get_price_command))
    dp.add_handler(CommandHandler('insert_entry', insert_entry_command))

    # add message reply handler
    dp.add_handler(MessageHandler(Filters.text, handle_message))

    # add error handler
    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()

main()