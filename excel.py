#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import logging
#
# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#                     level=logging.INFO)
#
# logger = logging.getLogger(__name__)


def findNRIC(mainlist, nric):
    listOfNRICIndices = []
    for i in range(0, 397):
        logger.info(nric, mainlist[i]['NRIC'].lower())
        if nric.lower() == mainlist[i]['NRIC'].lower():
            listOfNRICIndices.append(i)

    if len(listOfNRICIndices) == 1:
        return listOfNRICIndices[0]
    else:
        return False


def returnSeating(mainlist, nric):
    index = findNRIC(mainlist, nric)
    if index != False:
        mainlist[index]['GRP1_REG'] = 'P'
        return mainlist[index]['GRP1']

    return False


def saveFile(mainlist, worksheet, main_workbook):
    for i in range(0, 400):
        row_number = str(i + 2)
        worksheet['C' + str(row_number)].value = mainlist[i]['GRP1_REG']

    main_workbook.save('SeminarDatasheet.xlsx')
    # should only be run at end of bot life
