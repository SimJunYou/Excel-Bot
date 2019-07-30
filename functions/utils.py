#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from functions.init import PERSON, rList
from functions import excel

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


#######################


def validate_nric(nric):
    if len(nric) == 5:
        if nric[:4].isdigit() and nric[4].isalpha():
            return True
    return False


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
'''
    if update.message.chat_id == 234058962:
        update.message.reply_text(helpText)
    else:
        update.message.reply_text("You are not recognised!")


def attendanceStats(bot, update):
    if update.message.chat_id == 234058962:
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
    if update.message.chat_id == 234058962:
        update.message.reply_text("Good day, admin.\nTotal replies: {}".format(rList.llen('Feedback')))
        logger.info("Admin initiates stats report.\nTotal replies: {}".format(rList.llen('Feedback')))
    else:
        update.message.reply_text("You are not recognised!")


def sendAttendanceFile(bot, update):
    if update.message.chat_id == 234058962:
        update.message.reply_text("Good day, admin")
        logger.info("Admin requests latest attendance")
        excel.createFile_sem()
        bot.send_document(update.message.chat_id, document=open('Attendance.xlsx', 'rb'))
    else:
        update.message.reply_text("You are not recognised!")


def sendFeedbackFile(bot, update):
    if update.message.chat_id == 234058962:
        update.message.reply_text("Good day, admin")
        logger.info("Admin requests latest feedback")
        excel.createFile_fb()
        bot.send_document(update.message.chat_id, document=open('Feedback.xlsx', 'rb'))
    else:
        update.message.reply_text("You are not recognised!")

