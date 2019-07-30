#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler


from functions.init import rList, QN2, QN3, ENDPOST
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

reply_keyboard = [['Yes', 'No']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
remove = ReplyKeyboardRemove(remove_keyboard=True)


def postevent(bot, update):
    update.message.reply_text(
        ''' _Redesign Seminar Feedback_
*============================*
I'm here to give you some feedback prompts and collect your feedback. You may leave this chat at any time, it will not affect the bot.''',
        parse_mode='Markdown')
    update.message.reply_text("*Feedback prompt 1:*\nState and explain a segment of the seminar that was the most useful for you.",
                              parse_mode='Markdown')

    logger.info("User %s initiates contact", update.message.from_user.first_name)

    return QN2


def question2(bot, update, user_data):
    text = update.message.text
    user_data['Question1'] = text
    update.message.reply_text(
        "*Feedback prompt 2:*\nState and explain a segment of the seminar that was the _least_ useful for you.",
        parse_mode='Markdown')

    return QN3


def question3(bot, update, user_data):
    text = update.message.text
    user_data['Question3'] = text
    update.message.reply_text(
        "*Feedback prompt 3:*\nAny other comments? *Please leave your name* if you want us to get back to you.",
        parse_mode='Markdown')

    return ENDPOST

def endPost(bot, update, user_data):
    update.message.reply_text(
        "*Thank you for the feedback!*\nYou may now leave this chat.",
        parse_mode='Markdown')
    userFeedback = user_data['Question1']+'||||'+user_data['Question2']+'||||'+user_data['Question3']
    rList.rpush('Feedback', userFeedback)

    logger.info("User {} completes".format(update.message.from_user.first_name))
    user_data.clear()
    return ConversationHandler.END
