#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from functions.init import rList, ADMIN_TXT_START, ADMIN_END, ADMIN_FB_START
from functions import utils
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

admin_reply_keyboard = [['1', '2', '3', '4'], ['5', '6', '7', '8']]
admin_markup = ReplyKeyboardMarkup(admin_reply_keyboard, one_time_keyboard=True)
remove = ReplyKeyboardRemove(remove_keyboard=True)


#########


def startChangeChat(bot, update, user_data, args):
    updateMessage = "Good day, admin. You have requested to change the chat text. "\
                    "Which one of the 8 text prompts do you want to change?\n\n"\
                    "1. Start of attendance taking\n2. Wrong NRIC message\n3. End of attendance taking\n"\
                    "4. Start of feedback\n5. End of feedback"

    if update.message.from_user.id in utils.getAdminID():
        logger.info("Admin requests to change chat text")
        if not args:  # if arguments have not been passed, send update message and go to ADMIN_START
            update.message.reply_text(updateMessage, markup=admin_markup)
            return ADMIN_TXT_START
        else:
            # if arguments have been passed, pass arguments into receiveChatToChange
            return receiveChatToChange(bot, update, user_data, args[0])  # go straight to ADMIN_END or back to start
    else:
        update.message.reply_text("You are not recognised!")
        return ConversationHandler.END


def receiveChatToChange(bot, update, user_data, admin_state='0'):
    if admin_state not in ['1', '2', '3', '4', '5']:
        update.message.reply_text("Invalid number. Please try again.")
        return ADMIN_TXT_START  # go from start again to re-enter number

    admin_state = "TEXT" + admin_state  # in rList, the key is TEXT1 for the 'Start of attendance taking' text
    user_data["ADMIN_STATE"] = admin_state

    update.message.reply_text("The following is the current message:", reply_markup=remove)
    update.message.reply_text(utils.getChatText(admin_state), parse_mode='Markdown')

    if admin_state == "TEXT3":  # only text 3 needs the below for inserting the group number
        update.message.reply_text("Note: type *** where the group/seat number will go in the new message.")
    update.message.reply_text("Please type in your new message:")

    return ADMIN_END


#########


def startChangeFeedback(bot, update, user_data, args):
    updateMessage = "Good day, admin. You have requested to change the feedback questions."

    if update.message.from_user.id in utils.getAdminID():
        logger.info("Admin requests to change feedback questions")
        if not args:  # if arguments have not been passed, send update message and go to ADMIN_START
            update.message.reply_text(updateMessage, markup=admin_markup)
            return ADMIN_FB_START
        else:
            # if arguments have been passed, pass arguments into receiveChatToChange
            return receiveChatToChange(bot, update, user_data,
                                       args[0])  # go straight to ADMIN_END or back to ADMIN_START
    else:
        update.message.reply_text("You are not recognised!")
        return ConversationHandler.END


def receiveFeedbackToChange(bot, update, user_data, admin_state='0'):
    if admin_state not in ['1', '2', '3', '4', '5']:
        update.message.reply_text("Invalid number. Please try again.")
        return ADMIN_FB_START  # go from start again to re-enter number

    admin_state = "FEEDBACK" + admin_state  # in rList, the key is TEXT1 for the 'Start of attendance taking' text
    user_data["ADMIN_STATE"] = admin_state

    update.message.reply_text("The following is the current message:", reply_markup=remove)
    update.message.reply_text(utils.getChatText(admin_state), parse_mode='Markdown')

    if admin_state == "TEXT3":  # only text 3 needs the below for inserting the group number
        update.message.reply_text("Note: type *** where the group/seat number will go in the new message.")
    update.message.reply_text("Please type in your new message:")

    return ADMIN_END


#########


def updateChatText(bot, update, user_data):
    chatToChange = user_data["ADMIN_STATE"]
    newText = update.message.text
    rList.mset({chatToChange: newText})
    update.message.reply_text("The update is complete.")

    return ConversationHandler.END
