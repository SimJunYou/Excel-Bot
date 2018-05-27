import telegram
from telegram.ext import Updater, Filters, CommandHandler, MessageHandler, InlineQueryHandler
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import RegexHandler, ConversationHandler
import logging
import random

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# ---- setup ----
myToken = "241346491:AAH09_cf9KfaFohGgXUo96ljvOeyqcD1k4o"
bot = telegram.Bot(token=myToken)
updater = Updater(token=myToken)
dispatcher = updater.dispatcher

GENDER, PHOTO, LOCATION, BIO = range(4)

# ---- things ----
def start(bot, update):
    reply_keyboard = [['Boy', 'Girl', 'Other']]

    update.message.reply_text(
        'Hi! My name is Professor Bot. I will hold a conversation with you. '
        'Send /cancel to stop talking to me.\n\n'
        'Are you a boy or a girl?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return GENDER

def cancel(bot, update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END

conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],

    states={
        GENDER: [RegexHandler('^(Boy|Girl|Other)$', GENDER)]

##        PHOTO: [MessageHandler(Filters.photo, photo),
##                CommandHandler('skip', skip_photo)],
##
##        LOCATION: [MessageHandler(Filters.location, location),
##                   CommandHandler('skip', skip_location)],
##
##        BIO: [MessageHandler(Filters.text, bio)]
    },

    fallbacks=[CommandHandler('cancel', cancel)]
)

dispatcher.add_handler(conv_handler)

# ---- unknown command handler ----
# ---- must be added last! ----

def unknown(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="Unknown command!")

unknown_handler = MessageHandler([Filters.command], unknown)
dispatcher.add_handler(unknown_handler)

# ---- start ----

updater.start_polling()
print("running...")
updater.idle()
