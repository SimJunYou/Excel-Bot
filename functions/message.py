#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from functions.init import rList, ADMIN_TXT_START, ADMIN_END, ADMIN_FB_START, ADMIN_RM_END
from functions import utils
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

admin_reply_keyboard = [['1', '2'], ['3', '4', '5']]
removal_keyboard = ['Yes', 'No']
admin_markup = ReplyKeyboardMarkup(admin_reply_keyboard, one_time_keyboard=True)
removal_markup = ReplyKeyboardMarkup(removal_keyboard, one_time_keyboard=True)
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
    feedbackQuestions = utils.getFeedbackQuestions()
    if not feedbackQuestions:
        if update.message.from_user.id in utils.getAdminID():
            if not args:
                update.message.reply_text("There are no feedback questions to change. Please type 0 to add a question.")
                return ADMIN_FB_START
            else:
                receiveChatToChange(bot, update, user_data, args[0])
        else:
            update.message.reply_text("You are not recognised!")
            return ConversationHandler.END

    questionsMessage = ""
    for i in range(len(feedbackQuestions)):
        questionsMessage += "{}. Question {}\n".format(i, i)

    updateMessage = "Good day, admin. You have requested to change the feedback questions. " \
                    "Which one of the following feedback questions do you want to change?\n" \
                    "To add question, type 0. To remove question, type -(question number).\n" \
                    "For example, to remove question 2, type -2.\n\n"
    updateMessage += questionsMessage

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
    feedbackQuestions = utils.getFeedbackQuestions()

    if admin_state[0] == '-' and admin_state[1:].isdigit() and '0' < admin_state[1:] < str(len(feedbackQuestions)):
        admin_state = "QN" + admin_state  # in rList, the key is QN1 for the first feedback question
        user_data["ADMIN_STATE"] = admin_state
        update.message.reply_text("The following is the current question:", reply_markup=remove)
        update.message.reply_text(feedbackQuestions[admin_state], parse_mode='Markdown')
        update.message.reply_text("Confirm removal of question?\nYes/No:", reply_markup=removal_keyboard)
        return ADMIN_RM_END

    elif admin_state == '0':
        if not feedbackQuestions:
            admin_state = "QN1"
            # in rList, the key is QN1 for the first feedback question
        else:
            admin_state = "QN" + len(feedbackQuestions)
            # subsequent keys are QNn for the nth question
        user_data["ADMIN_STATE"] = admin_state
        update.message.reply_text("Please type your new question:")
        return ADMIN_END

    elif '0' < admin_state < str(len(feedbackQuestions)):
        admin_state = "QN" + admin_state  # in rList, the key is QN1 for the first feedback question
        user_data["ADMIN_STATE"] = admin_state
        update.message.reply_text("The following is the current question:", reply_markup=remove)
        update.message.reply_text(feedbackQuestions[admin_state], parse_mode='Markdown')
        update.message.reply_text("Please type in your new question:")
        return ADMIN_END

    else:
        update.message.reply_text("Invalid question number. Please try again.")
        return ADMIN_FB_START  # go from start again to re-enter number


#########


def updateChatText(bot, update, user_data):
    chatToChange = user_data["ADMIN_STATE"]
    newText = update.message.text

    if "QN" in chatToChange:  # if its a feedback question,
        rList.rpush("Feedback Questions", newText)  # rpush because new questions should go to end of list for order
        update.message.reply_text("The question update is complete.")
    else:  # otherwise, it is a message
        rList.mset({chatToChange: newText})  # just use mset with the ID
        update.message.reply_text("The update is complete.")

    return ConversationHandler.END


def removeQuestion(bot, update, user_data):
    chatToChange = user_data["ADMIN_STATE"]
    feedbackQuestions = utils.getFeedbackQuestions()
    del feedbackQuestions[chatToChange]

    rList.delete('Feedback Questions')
    for each in feedbackQuestions:
        rList.rpush('Feedback Questions', each)  # rpush because new questions should go to end of list for order
    update.message.reply_text("The removal is complete.")

    return ConversationHandler.END
