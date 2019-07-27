#!/usr/bin/env python
# -*- coding: utf-8 -*-

import openpyxl


def findNRIC(mainlist, nric):
    listOfNRICIndices = []
    for i in range(0, 400):
        if nric.lower() == mainlist[i]['NRIC'].lower():
            listOfNRICIndices.append(i)

    if len(listOfNRICIndices) == 1:
        return listOfNRICIndices[0]
    else:
        return False


def returnSeating(mainlist, nric):
    index = find_nric(mainlist, nric)
    if type(index) == int:
        mainlist[index]['GRP1_REG'] = 'P'
        return mainlist[index]['GRP1']

    return False


def saveFile(mainlist):
    for i in range(0, 400):
        row_number = str(i + 2)
        ws['C' + str(row_number)].value = mainlist[i]['GRP1_REG']

    main_workbook.save('SeminarDatasheet.xlsx')
    # should only be run at end of bot life