import xlrd
import re
import matplotlib.pyplot as plt
#from PyQt4 import QtCore, QtGui #in the pyqt4 tutorials
#from PyQt5 import QtCore, QtGui, QtWidgets #works for pyqt5
#from PyQt5.QtWidgets import QtGui, QtCore
#from PyQt5.QtWidgets import QtGui, QtCore

import sys

import string

def check_immr_untracked_task():
    xls_IMMR_Task_List = 'Y:\P_CommNav\Projects\IMMR_Airbus\Snapshot_Quantum\IMMR Airbus\ProjectHandbook\Financials\WeeklyActuals\Wkly_TT_Report\QueryResult.xls'
    xls_IMMR_ABM_Report = 'C:\\Users\\e427632\\Google Drive\\Lns\IMMR\\ABM_Report.xlsm'

    wk_task_list = xlrd.open_workbook(xls_IMMR_Task_List)
    sheet_task_list = wk_task_list.sheet_by_index(0)

    wk_abm_report = xlrd.open_workbook(xls_IMMR_ABM_Report)
    sheet_abm_task = wk_abm_report.sheet_by_name('Report')

    #get 2nd column from ABM Task
    taskABM = []
    for rownum in range(1, sheet_abm_task.nrows):
        taskABM.append(str(sheet_abm_task.cell(rownum, 2).value))
        temp = taskABM[-1]         #some_list[-n] syntax gets the nth-to-last element
        #print("[%s]" % temp)

        #if( temp.startswith('1AR000')):
        #    temp = temp[6:]
        temp = re.sub('1AR0*0','',temp)
        if( temp.endswith('.0')):
            temp = temp[:len(temp)-2]

        taskABM[-1] = temp

    #get 1st column from CQ Task List
    taskCQ = []
    for rownum in range(1, sheet_task_list.nrows):
        t = (str(sheet_task_list.cell(rownum,0).value),
             str(sheet_task_list.cell(rownum,1).value),
             str(sheet_task_list.cell(rownum, 2).value),
             str(sheet_task_list.cell(rownum, 7).value)
             )
        taskCQ.append(list(t))
        temp = taskCQ[-1][0]
        temp = re.sub('1AR0*0', '', temp)
        #if( temp.startswith('1AR000')):
        #    temp = temp[6:]

        taskCQ[-1][0] = temp


    task_in_y2016 = \
        [   '739',
            '746',
            '858',
            '13329',
            '13328',
            '6956',
            '7062',
            '7074',
            '7074',
            '7074',
            '7074',
            '7074',
            '7074',
            '7132',
            '7132',
            '7136',
            '7136',
            '7136',
            '7136',
            '7137',
            '7137',
            '7137',
            '7203',
            '7203',
            '7232',
            '7232',
            '7232',
            '7232',
            '7371',
            '7372',
            '7373',
            '7374',
            '7376',
            '7482',
            '7535',
            '7591',
            '7592',
            '7594',
            '7662',
            '7663',
            '11619',
            '11625',
            '13264',
            '13344',
            '13369',
            '11622',
            '13368',
            '13377',
            '10796',
            '11626',
            '13346',
            '13179',
            '13189',
            '13322',
            '13337',
            '13361',
            '11590',
            '12693',
            '13363',
            '13323',
            '13333',
            '13341',
            '12565',
            '11621',
            '13385',
            '13499',
            '13598',
            '14315',
            '14045',
            '14047',
            '13597',
            '13413',
            '13427',
            '14323',
            '13484',
            '13502',
            '13560',
            '13864',
            '14005',
            '13423',
            '13487',
            '13535',
            '13555',
        ]

    task_missed = [[]]
    for index in range(len(taskCQ)):
        rt = str_in_list((taskCQ[index])[0], taskABM)
        rt = rt or str_in_list((taskCQ[index])[0], task_in_y2016)

        if( not rt ):
            task_missed.append(taskCQ[index])
            print("\nmissed task ", taskCQ[index])


def str_in_list(astr, lst):
    rt = False
    for index in range( len(lst)):
        if( lst[index].find(astr) != -1):
            rt = True
            #print("task %s, index %d" % (astr, index))
            break
    #if( not rt):
        #print("missed task %s" % astr)

    return rt

#def msg_box(str1, str2):
    #QtWidgets.QMessageBox.about("My message box", "Text1 = %s, Text2 = %s" % ('T1', 'T2') )

if __name__ == '__main__':
    check_immr_untracked_task()
    #msg_box('1','2')