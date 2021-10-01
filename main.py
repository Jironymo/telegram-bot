from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import constants
import bot_funcs as funcs

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)


print('Bot starterd...')

def start_command(update, context):
    # context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")
    update.message.reply_text("I'm a bot, please talk to me!")

def help_command(update, context):
    # использую логику не из офф. источника, а: 
    # https://www.youtube.com/watch?v=PTAkiukJK7E
    # говорит, что контекст можно уже не предоставлять!
    update.message.reply_text("I'm under the water. Please, help me...")

def handle_message(update, context):
    text = update.message.text
    response = funcs.sample_responses(text)

    update.message.reply_text(response)

def error(update, context):
    print(f"Update {update} caused error {context.error}")

def main():
    updater = Updater(token=constants.BOT_TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start_command))
    dp.add_handler(CommandHandler('help', help_command))
    
    dp.add_handler(MessageHandler(Filters.text, handle_message))

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()

main()