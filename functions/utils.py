#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from functions.init import PERSON
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


def collectStats(bot, update):
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


def sendFile(bot, update):
    if update.message.chat_id == 234058962:
        update.message.reply_text("Good day, admin")
        logger.info("Admin requests latest file")
        excel.createFile()
        bot.send_document(update.message.chat_id, document=open('Attendance.xlsx', 'rb'))
    else:
        update.message.reply_text("You are not recognised!")

