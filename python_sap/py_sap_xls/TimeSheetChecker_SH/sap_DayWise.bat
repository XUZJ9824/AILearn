@echo off

rem Example1, sap_DayWise.bat "DAYWISE" "BJ" "373C100012" "" "SAP HTSC"
rem Example2, sap_DayWise.bat "DAYWISE" "SH" "385C100108" "" "SAP HTSC"

set filename=.\Export_Effort.vbs

set filepath= C:\Windows\SysWOW64\WScript.exe 

rem 	TCode_Name = WScript.Arguments.Item(0)     	
rem 	Site_Name =  WScript.Arguments.Item(1)
rem 	work_center = WScript.Arguments.Item(2) 
rem 	DestPath = WScript.Arguments.Item(3) 
rem 	SAPLoginProfile = WScript.Arguments.Item(4) 

set TCode_Name=%1 
set Site_Name=%2 
set work_center=%3 
set DestPath=%cd%\
set SAPLoginProfile=%5

echo "Start DayWise batch, "

echo tcode %TCode_Name%
echo site %Site_Name%
echo work_center %work_center%
echo dest_path %DestPath%
echo sap_profile %SAPLoginProfile%


if not exist "C:\Temp" mkdir C:\Temp

del /F *.XLSX
del /F C:\Temp\*.xls*

rem if exist C:\Windows\SysWOW64\WScript.exe (start %filepath%%filename% %1 %2 %3 %4 %5 cd) else (start %filename% %1 %2 %3 %4 %5 cd)

if exist C:\Windows\SysWOW64\WScript.exe (start /B /MIN /WAIT %filepath%%filename% %TCode_Name% %Site_Name% %work_center% %DestPath% %SAPLoginProfile% cd) else (start /B /MIN /WAIT %filename% %TCode_Name% %Site_Name% %work_center% %DestPath% %SAPLoginProfile% cd)




