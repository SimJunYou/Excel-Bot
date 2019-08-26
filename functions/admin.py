#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from functions.init import rList, NEW_ADMIN
from functions import utils
from telegram.ext import ConversationHandler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def startNewAdmin(bot, update):
    updateMessage = "Good day, admin. You have requested to add a new admin. " \
                    "Please send me his/her contact so that I can register them in the system."

    if update.message.from_user.id in utils.getAdminID():
        logger.info("Admin requests to add new admin")
        update.message.reply_text(updateMessage)
        return NEW_ADMIN
    else:
        update.message.reply_text("You are not recognised!")
        return ConversationHandler.END


def addNewAdmin(bot, update):
    #  below is to read the info from the new admin contact sent by admin
    userID = update.effective_message.contact.user_id
    userName = update.effective_message.contact.first_name
    userPhone = update.effective_message.contact.phone_number

    logger.info("New admin: " + str(userID) + " " + userName + " " + str(userPhone))
    #  admin list holds all admin ids + admin names + phone numbers
    rList.lpush('Admin List', str(userID) + "|" + userName + "|" + str(userPhone))

    logger.info("New admin {} has been added.".format(userName))
    update.message.reply_text("New admin {} has been added.".format(userName))

    return ConversationHandler.END


def deleteAllAdmins(bot, update):
    if update.message.from_user.id in utils.getAdminID():
        rList.delete('Admin List')
        rList.lpush('Admin List', "234058962|JunYou|+6584687298")
        logger.info("Deleted all admins except JunYou")
        update.message.reply_text("Deleted all admins except JunYOu")
    else:
        update.message.reply_text("You are not recognised!")


def listAllAdmins(bot, update):
    adminList = ""
    if update.message.from_user.id in utils.getAdminID():
        for i in range(rList.llen('Admin List')):
            adminInfo = rList.lindex('Admin List', i).decode('utf-8').split("|")
            logger.info(": ".join(adminInfo[1:]))
            adminList += ": ".join(adminInfo[1:]) + "\n"  # search, decode, split, slice, join, and concatenate

        if adminList != "":
            logger.info(adminList)
            update.message.reply_text(adminList)  # send the complete list
        else:
            update.message.reply_text("There are no admins")
    else:
        update.message.reply_text("You are not recognised!")


def removeAdmin(bot, update, args):
    if not args:
        update.message.reply_text("Please provide a name. e.g. /removeAdmin John")
        return

    searchName = args[0]  # there should be no space in the first name
    removed = False
    if update.message.from_user.id in utils.getAdminID():
        for i in range(rList.llen('Admin List')):
            current = rList.lindex('Admin List', i).decode('utf-8')
            logger.info(current)
            if searchName.lower() in current.lower():  # if the name is found
                removed = current
                if searchName != "JunYou":
                    rList.lrem('Admin List', 1, current)  # remove one object with same name, searching from head
            break

    if not removed:
        update.message.reply_text("Admin {} not found".format(searchName))
    else:
        removedName, removedPhone = removed.split("|")[1:]
        logger.info("Admin {} (p/h: {}) has been removed.".format(removedName, removedPhone))
        update.message.reply_text("Admin {} (p/h: {}) has been removed".format(removedName, removedPhone))