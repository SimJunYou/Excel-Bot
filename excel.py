#!/usr/bin/env python
# -*- coding: utf-8 -*-

import openpyxl

        
def find_nric(mainlist, nric):
    listOfNRICIndices = []
    for i in range(0,308):
        if nric.lower() == mainlist[i]['NRIC'].lower():
            listOfNRICIndices.append(i)

    if len(listOfNRICIndices) == 1:
        return listOfNRICIndices[0]
    else:
        return listOfNRICIndices


def return_seating(mainlist, nric):
    index = find_nric(mainlist, nric)
    if type(index) == int:
        if mainlist[index]['GRP1_REG'] == '':
            mainlist[index]['GRP1_REG'] = 'P'
            return mainlist[index]['GRP1']
        elif mainlist[index]['GRP2_REG'] == '':
            mainlist[index]['GRP2_REG'] = 'P'
            return mainlist[index]['GRP2']

    return False
        
def saveFile(mainlist):
    for i in range(0,308):
        row_number = str(i+2)
        ws['E'+str(row_number)].value = PERSON[i]['GRP1_REG']
        ws['G'+str(row_number)].value = PERSON[i]['GRP2_REG']

    main_workbook.save('SeminarDatasheet.xlsx')
            
        
