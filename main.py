#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)

from openpyxl import load_workbook

import logging
import os, redis

from functions import excel, seminar, post_seminar, utils

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# <EXCEL AND REDIS>
logger.info("Opening Excel file")
main_workbook = load_workbook('SeminarDatasheet.xlsx')
ws = main_workbook['Sheet1']

rList = redis.from_url(os.environ.get("REDIS_URL"))
PERSON = []  # PERSON for local work, redis for heroku database

excel.dumpExcel(ws)

logger.info("Excel file dumped into working list and redis")
main_workbook.save('SeminarDatasheet.xlsx')
logger.info("Excel file closed")
# </EXCEL AND REDIS>


# init values for Telegram
TYPING_NRIC, RESPONSE = range(2) # for conv_handler
QN1, QN2, QN3 = range(3) # for post_conv_handler
reply_keyboard = [['Yes', 'No']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
remove = ReplyKeyboardRemove(remove_keyboard=True)


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater("241346491:AAH09_cf9KfaFohGgXUo96ljvOeyqcD1k4o")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states TYPING_NRIC and RESPONSE
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', seminar.start)],
        states={
            TYPING_NRIC: [MessageHandler(Filters.text,
                                         seminar.get_nric,
                                         pass_user_data=True)],
            RESPONSE: [RegexHandler('^Yes|No$',
                                    seminar.final,
                                    pass_user_data=True)]
        },
        fallbacks=[]
    )

    # # Add conversation handler with the states QN1, QN2, QN3
    # post_conv_handler = ConversationHandler(
    #     entry_points=[CommandHandler('postevent', post_seminar.postevent)],
    #     states={
    #         QN1: [MessageHandler(Filters.text,
    #                                      get_nric,
    #                                      pass_user_data=True)],
    #         QN2: [MessageHandler(Filters.text,
    #                              get_nric,
    #                              pass_user_data=True)],
    #         QN3: [MessageHandler(Filters.text,
    #                              get_nric,
    #                              pass_user_data=True)]
    #     },
    #     fallbacks=[]
    # )

    dp.add_handler(conv_handler)
    # dp.add_handler(post_conv_handler)
    dp.add_handler(CommandHandler('stats', utils.collectStats))
    dp.add_handler(CommandHandler('file', utils.sendFile))

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
