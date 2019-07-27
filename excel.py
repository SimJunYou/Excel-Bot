#!/usr/bin/env python
# -*- coding: utf-8 -*-

def findNRIC(mainlist, nric):
    listOfNRICIndices = []
    for i in range(0, 398):
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
    for i in range(0, 398):
        row_number = str(i + 2)
        worksheet['C' + str(row_number)].value = mainlist[i]['GRP1_REG']

    main_workbook.save('SeminarDatasheet.xlsx')
    # should only be run at end of bot life
