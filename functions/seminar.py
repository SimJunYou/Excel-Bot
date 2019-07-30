#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler


from functions.init import PERSON, TYPING_NRIC, RESPONSE
from functions import excel, utils
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

reply_keyboard = [['Yes', 'No']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
remove = ReplyKeyboardRemove(remove_keyboard=True)


def start(bot, update):
    update.message.reply_text(
        ''' _Welcome to the Redesign Seminar!_
*============================*
I'm here to mark your attendance and provide your assigned group. You may leave this chat at any time, it will not affect the bot.

Please enter the _last 5 characters_ of your NRIC:''',
        parse_mode='Markdown')

    logger.info("User %s initiates contact", update.message.from_user.first_name)

    return TYPING_NRIC


def get_nric(bot, update, user_data):
    text = update.message.text
    user_data['NRIC'] = text.upper()
    if utils.validate_nric(text):
        update.message.reply_text(
            "To confirm, the last 5 characters of your NRIC are {}.\n\nIs this correct? Yes/No".format(text),
            reply_markup=markup)

        return RESPONSE

    else:
        update.message.reply_text(
            "*The provided partial NRIC {} is incorrect!* Please check that it is in the format 1234E (where full NRIC would be S9951234E)\n\nLet's try again. Last 5 characters of your NRIC:".format(
                text),
            parse_mode='Markdown')

        return TYPING_NRIC


def final(bot, update, user_data):
    text = update.message.text
    if text.lower() == "yes":
        # MAIN ACTION
        seating = excel.returnSeating(PERSON, user_data['NRIC'])
        if seating is None:
            update.message.reply_text(
                "We cannot find your NRIC, please look for assistance around the venue.\n\nYou may now leave this chat or type /start to register another NRIC entry",
                reply_markup=remove)
        else:
            seating = seating.upper()
            update.message.reply_text(
                '''Your assigned group is: {}.\n\nThank you for attending this seminar! You may now leave this chat or type /start to register another NRIC entry.'''.format(
                    seating),
                reply_markup=remove)
    elif text.lower() == "no":
        update.message.reply_text("Let's try again. Enter the last 5 digits of your NRIC:", reply_markup = remove)
        return TYPING_NRIC

    logger.info("User {} completes".format(update.message.from_user.first_name))
    user_data.clear()
    return ConversationHandler.END
