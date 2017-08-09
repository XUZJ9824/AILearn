'''
Created on Aug 12, 2016

@author: E427632
'''

#TBD temp share path like xls_file = \\Ch01w0103\CNSCOE\Process\SAP\Effort_2016;
#TBD recipient = 'zhijian.xu@honeywell.com;';
#TBD compile to exe;
#TBD config file read by python;

#import os;
import subprocess
import xlrd
import time
#import xlwt;
import io
import win32com.client
import os, sys
import time
if sys.version_info[0] >=  3:
    import configparser
else:
    import ConfigParser
    
#from ctypes.test.test_errno import threading
import smtplib
from io import StringIO
from email.mime.text import MIMEText  
#-------------------------------------------------------------------------
#from win32com.client import Dispatch, constants;-
# Import smtplib for the actual sending function
#import smtplib;
# Import the email modules we'll need
#from email.mime.multipart import MIMEMultipart;
#from email.mime.text import MIMEText;
#from O365 import Message;
#------------------------------------------------------------------------
Daywise_Effort_filename = 0
location_make = 0
location_bat = 0
Site_Name = 0
Work_Center = 0
recipient = 0
SAP_Profile_Str = 0
mailMsg = StringIO();

#------------------- all use-----------------------------------------------------------
CHECK_RESULT = 1;
SAP_KEY = "DAYWISE"

#####################################
#from win32com.client import Dispatch
#xl = Dispatch('Excel.Application')
#wb = xl.Workbooks.Open('C:\\Documents and Settings\\GradeBook.xls')
#xl.Visible = True
#####################################

############Check Un-Approved Timesheet BJ#############################
def Check_Daywise_UnApproved_TimeCheck(strDayWisePath):

    #strTemp="\n Check result for File %s : \n" % (strDayWisePath);
    strTemp = "Check result for File "+strDayWisePath+","
    print(strTemp);
  
    wkbook = xlrd.open_workbook(strDayWisePath);    
    worksheet = wkbook.sheet_by_index(0);    
    msg= ''
    msg = strTemp
    for row in range(6, 65535):                
        if row >= worksheet.nrows:
            break;
        else:
            valEmpID = worksheet.cell(row,4).value;
            valEmpName = worksheet.cell(row,5).value;
            valWeekDay = worksheet.cell(row, 6).value;
            valStatus =worksheet.cell(row,15).value;
            valTargetHours = worksheet.cell(row, 18).value;
            if valStatus != "Approved" and valStatus != "Locked":
                print('\tEmplID', int(valEmpID), '\tEmpName', valEmpName, '\tStatus', valStatus, '\tTargetHours', int(valTargetHours), '\tWeekDay', valWeekDay);
                strTemp = "\nEmplID: %s,\tEmpName: %s, \tStatus: %s, \tTargetHrs: %s, \tWeekDay: %s" % (valEmpID, valEmpName, valStatus, valTargetHours, valWeekDay);
                msg= msg +strTemp
    print(msg)
    return msg

def send_mail_via_com(text, subject, recipient, profilename="Outlook2013"): 
    print(text)
    const=win32com.client.constants
    olMailItem = 0x0
    obj = win32com.client.Dispatch("Outlook.Application")
    newMail = obj.CreateItem(olMailItem)
    newMail.Subject = subject
    newMail.Body = text
    newMail.To = recipient
    #attachment1 = r"c:\all_req.xlsx"
     
    #newMail.Attachments.Add(Source=attachment1)
    newMail.display()
    newMail.Send()
    print("send_mail_via_com done")

def Daywise_Effort_Process():    
    global SAP_KEY,location_bat,Site_Name,Work_Center,Daywise_Effort_filename,location_make,SAP_Profile_Str
    print('Daywise_Effort_Process work ', Daywise_Effort_filename)
    
    sleepCount = 30 # sleep 30 times, 2 minutes every time
    fileExist = os.path.exists(Daywise_Effort_filename)
    if fileExist == True:
        os.remove(Daywise_Effort_filename)
        fileExist = os.path.exists(Daywise_Effort_filename)	
       
    location_make = location_make + "\\"
  
    location_bat = ".\sap_DayWise_Ex.bat"
    #os.system(location_bat + " \"DAYWISE\" \"" + City_key +"\" \""+ WORK_CENTER+"\" \"" + location_make +"\"")   
    os.system(location_bat + " \"DAYWISE\" \"" + Site_Name +"\" \""+ Work_Center+"\" \"" + location_make + "\" \"" + SAP_Profile_Str + "\"")
    
    print(location_bat+ " \"DAYWISE\" \"" + Site_Name + "\" \"" + Work_Center +"\" \""+ location_make + "\" \"" + SAP_Profile_Str + "\"")     
    fileExist_Time = False

    while(fileExist_Time == False and sleepCount>=1):
        time.sleep(30)
        sleepCount = sleepCount - 1
        fileExist = os.path.exists(Daywise_Effort_filename)
        print ('fileExist ', fileExist, ', sleepCount ', sleepCount, ' filePathName ', Daywise_Effort_filename)
        fileExist_Time = os.path.exists(Daywise_Effort_filename)     


def get_file_infor():
    global Daywise_Effort_filename,location_make,location_bat,Site_Name,Work_Center,recipient,SAP_Profile_Str

    file = open(".\config.txt")
    counter = 0

    while 1:
        line = file.readline()
        counter = counter +1
        if counter == 2:
            location_bat = line
            #print("location_bat",location_bat)
            splitLine = os.path.split(line)   
            location_bat = splitLine[0]
            print("location_bat:",location_bat)
            #print("location_bat",splitLine[1])
        elif counter == 5:
            Daywise_Effort_filename = line
            Daywise_Effort_filename = os.path.split(line)   
            Daywise_Effort_filename = Daywise_Effort_filename[0]
            print("Daywise_Effort_filename:",Daywise_Effort_filename)
            splitLine2 = os.path.split(Daywise_Effort_filename)   
            location_make = splitLine2[0]
            print("location_make:",location_make)
        elif counter == 8:     
            splitLine_city = os.path.split(line)   
            Site_Name = splitLine_city[0]
            print("Site_Name:",Site_Name)
        elif counter == 11:
            Work_Center = line
            splitLine_wprok = os.path.split(line)   
            Work_Center = splitLine_wprok[0]
            print("Work_Center:",Work_Center)    
        elif counter == 14:
            recipient = line
            splitLine_rec = os.path.split(line)   
            recipient = splitLine_rec[0]
            print("recipient:",recipient)
        elif counter == 17:
            SAP_Profile_Str = line
            splitLine_rec = os.path.split(line)   
            SAP_Profile_Str = splitLine_rec[0]
            print("SAP_Profile_Str:",SAP_Profile_Str) 
        if not line:

            break
    file.close()
    pass # do something

def get_configfile_infor(): 
    global Daywise_Effort_filename,location_make,location_bat,Site_Name,Work_Center,recipient,SAP_Profile_Str
    tfile=open(".\config.txt",'r')
    lines = tfile.readlines() 
    flen=len(lines)-1 
    #sstr = ['[Daywise_Effort_file location]','[Site]', '[Work Center]', '[Mail Recipient]', '[SAP Profile Name]']
    sstr = ['[Site]', '[Work Center]', '[Mail Recipient]', '[SAP Profile Name]']
    counter = 0
    result = 0

    for i in range(flen):
        if  sstr[counter] in lines[i]:
            #print "line",lines[i]          
            result = lines[i+2]
            #print "result",result     
            '''     
            if counter == 0:
                Daywise_Effort_filename = result
                Daywise_Effort_filename = os.path.split(result)   
                Daywise_Effort_filename = Daywise_Effort_filename[0]
                print("Daywise_Effort_filename:",Daywise_Effort_filename)
                splitLine2 = os.path.split(Daywise_Effort_filename)   
                location_make = splitLine2[0]
                print("location_make:",location_make)
            '''
            if counter == 0:           
                Site_Name = result 
                str_list=list(Site_Name) 
                str_list.pop()
                Site_Name = "".join(str_list)
                print("Site_Name:",Site_Name)
            elif counter == 1:
                Work_Center = result
                str_list=list(Work_Center) 
                str_list.pop()
                Work_Center = "".join(str_list)
                print("WORK_CENTER:",Work_Center)    
            elif counter == 2:
                recipient = result
                str_list=list(recipient) 
                str_list.pop()
                recipient = "".join(str_list)
                print("recipient:",recipient)    
            elif counter == 3:
                SAP_Profile_Str = result
                str_list=list(SAP_Profile_Str) 
                str_list.pop()
                SAP_Profile_Str = "".join(str_list)
                print("SAP_Profile_Str:",SAP_Profile_Str)     
            counter= counter +1
            
        if counter > 3:  
            tfile.close()                 
            break 


if __name__ == '__main__':
    try:
        get_configfile_infor()
        Daywise_Effort_filename = os.getcwd() + "\\" + Site_Name + "_" + Work_Center + "_Daywise_Effort.XLSX"
        print("get_configfile_infor",Daywise_Effort_filename)
        splitLine2 = os.path.split(Daywise_Effort_filename)
        location_make = splitLine2[0]
        print("location_make:",location_make)
        Daywise_Effort_Process()
        MsgOutlook = Check_Daywise_UnApproved_TimeCheck(Daywise_Effort_filename)
        send_mail_via_com(MsgOutlook, 'Timesheet Approval Check', recipient)
        mailMsg.close()
    except:
        print("Error:", sys.exc_info()[0])
        raise

  
    
