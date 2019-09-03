#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler

from functions.init import rList, QUESTION, ENDPOST
from functions import utils
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

reply_keyboard = [['Yes', 'No']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
remove = ReplyKeyboardRemove(remove_keyboard=True)


def postevent(bot, update, user_data):
    update.message.reply_text(utils.getChatText("TEXT4"), parse_mode='Markdown')
    logger.info("User %s initiates contact", update.message.from_user.first_name)
    user_data['Question'] = utils.getQuestions()  # retrieve list of feedback questions
    user_data['Answer'] = '0'  # first answer flag
    update.message.reply_text(user_data['Question'][0], parse_mode='Markdown')

    return QUESTION


def question(bot, update, user_data):
    text = update.message.text
    if user_data['Answer'] != '0':  # if it is not the first question in the list
        user_data['Answer'] += "|||" + text  # put separator with the feedback answer
    else:  # if it is the first question in the list
        user_data['Answer'] = text  # don't need separator with the feedback answer

    user_data['Question'] = user_data['Question'][1:]  # remove the first question, since it's been asked
    if not user_data['Question']:
        return ENDPOST
    update.message.reply_text(user_data['Question'][0], parse_mode='Markdown')
    return QUESTION


def endPost(bot, update, user_data):
    text = update.message.text
    user_data['Question3'] = text
    update.message.reply_text(utils.getChatText("TEXT5"), parse_mode='Markdown')
    rList.rpush('Feedback', user_data['Answer'])

    logger.info("User {} completes".format(update.message.from_user.first_name))
    user_data.clear()
    return ConversationHandler.END
