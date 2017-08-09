'''
Created on Aug 31, 2016

@author: E427632
'''
#For Py2Exe, which not comply with Python 3.6 and later

#from distutils.core import setup;
#import py2exe;

#setup(console=['sap_timesheet_checker.py'], options = {'py2exe': { 'packages':['requests']}});
    
import sys
from cx_Freeze import setup,Executable
build_exe_options = {"packages": ["os"], "excludes": ["tkinter"]}
base = None
if sys.platform == "win32":
    base = "Win32GUI"
setup(
    name = "HTSC_SAP_Timesheet_Checker",
    version = "0.1",
    descriptiom = "HTSC SAP Timesheet Checker",
    options = {"build_exe": build_exe_options},
    executables = [Executable("sap_timesheet_checker.py")])