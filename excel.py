#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging, threading

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def findNRIC(mainlist, nric):
    listOfNRICIndices = []
    for i in range(0, 399):
        if nric.lower() == mainlist[i]['NRIC'].lower():
            listOfNRICIndices.append(i)

    if len(listOfNRICIndices) == 1:
        return listOfNRICIndices[0]
    else:
        return None


def returnSeating(mainlist, nric):
    index = findNRIC(mainlist, nric)
    if index != None:
        mainlist[index]['GRP1_REG'] = 'P'
        return mainlist[index]['GRP1']

    return None


def saveFile(mainlist, worksheet, main_workbook):
    for i in range(0, 399):
        row_number = str(i + 2)
        worksheet['C' + str(row_number)].value = mainlist[i]['GRP1_REG']
    logger.info("saveFile is run")
    main_workbook.save('SeminarDatasheet.xlsx')
    # should only be run at end of bot life
