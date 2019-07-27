#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram import ReplyKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)

import logging, threading

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

#################

# EXCEL BITS

from openpyxl import load_workbook
from excel import returnSeating, saveFile

# read working copy of the workbook
main_workbook = load_workbook('SeminarDatasheet.xlsx')
ws = main_workbook['Sheet1']

# dump all info values into PERSON dict array for access
PERSON = []
for i in range(2,400):
    row_number = str(i)
    PERSON.append( {'NRIC': ws['A'+str(row_number)].value,
                    'GRP1': ws['B'+str(row_number)].value,
                    'GRP1_REG': ''})


#################

TYPING_NRIC, RESPONSE = range(2)
reply_keyboard = [['Yes', 'No']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

def start(bot, update):
    update.message.reply_text("Welcome to the Redesign Seminar.")
    update.message.reply_text("Last 5 digits of your NRIC:")

    logger.info("User %s initiates contact", update.message.from_user.first_name)

    return TYPING_NRIC


def validate_nric(nric):
    if len(nric) == 5:
        if nric[:4].isdigit() and nric[4].isalpha():
            return True
    return False


def get_nric(bot, update, user_data):
    text = update.message.text
    user_data['NRIC'] = text
    if validate_nric(text):
        update.message.reply_text(
            'To confirm, the last 5 digits of your NRIC are {}'.format(text))
        update.message.reply_text('Is this correct? Yes/No', reply_markup=markup)

        return RESPONSE
    
    else:
        update.message.reply_text(
            'The provided partial NRIC {} is incorrect.'.format(text))
        update.message.reply_text(
            'Please check that it is in the format 1234E (where full NRIC would be S9951234E)')

        update.message.reply_text("Last 5 digits of your NRIC:")
        
        return TYPING_NRIC


def final(bot, update, user_data):
    text = update.message.text
    if text.lower() == "yes":
        #MAIN ACTION
        seating = returnSeating(PERSON, user_data['NRIC'])
        if seating == None:
            update.message.reply_text("Your NRIC is not in the list. Please look for ___")
        else:
            update.message.reply_text("Your seating is: {}".format(seating))
    elif text.lower() == "no":
        update.message.reply_text("Last 5 digits of your NRIC:")
        return TYPING_NRIC

    logger.info("User {}{} completes".format(update.message.from_user.last_name, update.message.from_user.first_name))
    user_data.clear()
    return ConversationHandler.END

###############

def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)

###############

def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater("241346491:AAH09_cf9KfaFohGgXUo96ljvOeyqcD1k4o")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            TYPING_NRIC: [MessageHandler(Filters.text,
                                           get_nric,
                                           pass_user_data=True),
                            ],

            RESPONSE: [RegexHandler('^Yes|No$',
                                          final,
                                          pass_user_data=True),
                       ],
        },

        fallbacks=[]
    )


    def shutdown():
        updater.stop()
        updater.is_idle = False

    def killBot(bot, update):
        if update.message.chat_id == 234058962:
            update.message.reply_text("Saving memory to Excel file...")
            saveFile(PERSON, ws, main_workbook)
            update.message.reply_text("Bot is being killed")
            logger.info("Bot has been killed")
            updater.stop()
        else:
            update.message.reply_text("You are not recognised!")



    dp.add_handler(conv_handler)
    dp.add_handler(CommandHandler('kill', killBot))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()
    logger.info("The bot is running.")
    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
