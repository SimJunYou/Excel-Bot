#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from functions.init import PERSON, rList
from functions import excel
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

admin_reply_keyboard = [['1', '2', '3', '4'], ['5', '6', '7', '8']]
admin_markup = ReplyKeyboardMarkup(admin_reply_keyboard, one_time_keyboard=True)
remove = ReplyKeyboardRemove(remove_keyboard=True)

#######################


def validate_nric(nric):
    if len(nric) == 5:
        if nric[:4].isdigit() and nric[4].isalpha():
            return True
    return False


def getAdminID():
    adminList = []
    for i in range(rList.llen('Admin List')):
        adminInfo = rList.lindex('Admin List', i).decode('utf-8').split("|")
        adminID = adminInfo[0]
        adminList.append(int(adminID))
    return adminList


def getFeedbackQuestions():
    questionsList = {}
    for i in range(rList.llen('Feedback Questions')):
        question = rList.lindex('Feedback Questions', i).decode('utf-8')
        questionID = "QN"+str(i+1)
        questionsList[questionID] = question

    if questionsList == {}:
        return False
    return questionsList


def adminHelp(bot, update):
    helpText = '''AVAILABLE COMMANDS:
    
Attendance stats - /aStats
Gives you the total and currently registered number of participants.

Feedback stats - /fStats
Gives you the current number of feedback responses.

Attendance file - /aFile
Sends you the most updated Excel file for attendance.

Feedback file - /fFile
Sends you the most updated Excel file for feedback.

Add new admin - /newAdmin
Lets you add a new admin by sending their contact to the bot.

List all admins - /listAdmins
Shows you all the current admins and their phone numbers.

Remove an admin - /removeAdmin
Lets you remove an admin.
'''
    if update.message.from_user.id in getAdminID():
        update.message.reply_text(helpText)
    else:
        update.message.reply_text("You are not recognised!")


def attendanceStats(bot, update):
    if update.message.from_user.id in getAdminID():
        count = 0
        total = 0
        for each in PERSON:
            total += 1
            if each['GRP1_REG'] == 'P':
                count += 1
        update.message.reply_text("Good day, admin.\nTotal: {}, Present: {}".format(total, count))
        logger.info("Admin initiates stats report.\nTotal: {}, Present: {}".format(total, count))
    else:
        update.message.reply_text("You are not recognised!")


def feedbackStats(bot, update):
    if update.message.from_user.id in getAdminID():
        update.message.reply_text("Good day, admin.\nTotal replies: {}".format(rList.llen('Feedback')))
        logger.info("Admin initiates stats report.\nTotal replies: {}".format(rList.llen('Feedback')))
    else:
        update.message.reply_text("You are not recognised!")


def chatID(bot, update):
    update.message.reply_text(update.message.from_user.id)


def sendAttendanceFile(bot, update):
    if update.message.from_user.id in getAdminID():
        update.message.reply_text("Good day, admin")
        logger.info("Admin requests latest attendance")
        excel.createFile_sem()
        bot.send_document(update.message.chat_id, document=open('Attendance.xlsx', 'rb'))
    else:
        update.message.reply_text("You are not recognised!")


def sendFeedbackFile(bot, update):
    if update.message.from_user.id in getAdminID():
        update.message.reply_text("Good day, admin")
        logger.info("Admin requests latest feedback")
        excel.createFile_fb()
        bot.send_document(update.message.chat_id, document=open('Feedback.xlsx', 'rb'))
    else:
        update.message.reply_text("You are not recognised!")


def getChatText(message):
    chatText = rList.get(message)
    return chatText


def getQuestions():
    questionList = []
    for index in range(rList.llen('Feedback Questions')):
        questionList.append(rList.lindex('Feedback Questions'))
    return questionList


