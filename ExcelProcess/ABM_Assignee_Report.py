# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 13:40:26 2017

@author: E427632
"""

#import subprocess
import xlrd
#import time
#import string
#import xlwt;
#import io
#import win32com.client
import os
#import date
import datetime
#if sys.version_info[0] >=  3:
#    import configparser
#else:
#    import ConfigParser

Engineer_List = ['Yan', 
'Murphy', 
'Michael', 
'Chongyang', 
'Mingyi', 
'Jie', 
'Weilong', 
'Xu', 
'Mingquan'];

def Report_ABM(strAssignee, strABMPathFile):
    #print(os.path.basename(strABMPathFile));
    try:
        book = xlrd.open_workbook(strABMPathFile,on_demand=True);
    
    except Exception as e:
        print("Error: ", os.path.basename(strABMPathFile), str(e));
        return;
    
    sheet = book.sheet_by_name('Data');
    rowIndex = 6; #Starting first task row
    colIndex = 28; #Responsible Person, column start with 0
    
    for rowIndex in range(6, 100):                
        if rowIndex >= sheet.nrows:
            break;
        else:
            varAssignee = str(sheet.cell(rowIndex, colIndex).value);
            #print(varAssignee);
            
            #if varAssignee == strAssignee:
            if strAssignee in varAssignee:
            #if sheet.cell(rowIndex, colIndex).contains('Yan'):
                varSCRID = str(sheet.cell(rowIndex,4).value);
                varTaskID = str(sheet.cell(rowIndex,5).value);
                
                date = sheet.cell_value(rowIndex,23)
                varPStart = datetime.datetime(*xlrd.xldate_as_tuple(date, book.datemode));
                
                date = sheet.cell_value(rowIndex,24)
                varPEnd = datetime.datetime(*xlrd.xldate_as_tuple(date, book.datemode));               
                
                varPercentage = str(sheet.cell(rowIndex,27).value)
                print(os.path.basename(strABMPathFile), "|\t", 
                      varAssignee, "|\t", 
                      varSCRID, "|\t", 
                      varTaskID, "|\t",
                      varPStart, "|\t", 
                      varPEnd, "|\t", 
                      varPercentage)    
    
    book.unload_sheet('Data');
    
    
def Report_ABM_Folder(strAssignee, strFolder):
    for filename in os.listdir(strFolder):
        if (not filename.startswith("~$")) and filename.endswith(".xlsm"): 
            #print(os.path.join(strFolder, filename))
            Report_ABM(strAssignee,os.path.join(strFolder, filename))
        else:
            continue    
    
if __name__ == '__main__':
    global Engineer_List;
    print("ABM", "|\t", 
    "Assignee", "|\t", 
    "SCRID", "|\t", 
    "TaskID", "|\t", 
    "Start","|\t", 
    "End", "|\t", 
    "Percentage")    
    for eng in Engineer_List:
        Report_ABM_Folder(eng, 'Y:\P_CommNav\Projects\IMMR_Airbus\Snapshot_Quantum\IMMR Airbus\ProjectHandbook\ABMs\ABMS')
    print("END")