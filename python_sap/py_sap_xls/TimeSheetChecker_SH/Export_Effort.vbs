REM: we must change SAPGUI option ( Alt+F12 ) to disable warning dialogue 
REM: when a SAP script connect to SAP GUI.


rem: input parameters,
dim Site_Name
dim work_center
dim TCode_Name
dim DestPath
dim SAPLoginProfile

rem: global variables,
dim bChoseManulMonth
dim Plant_Code
dim curYear
dim curMonth
dim curDay

dim Application
dim Connection
dim session

call main_proc()

public Sub main_proc()  	
    curYear = year(Now)
    curMonth = Month(Now)
    curDay = Day(Now)

	TCode_Name = WScript.Arguments.Item(0)     	
	Site_Name =  WScript.Arguments.Item(1)
	work_center = WScript.Arguments.Item(2) 
	DestPath = WScript.Arguments.Item(3) 
	SAPLoginProfile = WScript.Arguments.Item(4) 
		
	bChoseManulMonth = 0 Rem: switch manual month or auto mode.

	if( bChoseManulMonth = 1 ) then
		inputFiscalM = Inputbox("Input Fiscal Month")

		if( not isempty(inputFiscalM) ) then
			 curMonth = inputFiscalM
			 curDay = 10
		end if
	end if

	Set Application = CreateObject("Sapgui.ScriptingCtrl.1")
	Set Connection  = Application.OpenConnection(SAPLoginProfile, True)
	Set session     = Connection.Children(0)

	'On error resume next

	If TCode_Name = "DAYWISE" Then	        
			select case Site_Name
				case "SH"
					Plant_Code = "385C"					 
					Generate_Daywise_Report
				case "BJ"
					Plant_Code = "373C"					 
					Generate_Daywise_Report
			    case "ALL"
					Plant_Code = "385C"					 
					Generate_Daywise_Report
					Plant_Code = "373C"					 
					Generate_Daywise_Report
			    default:
				    Msgbox "Invalid Site Name " & Site_Name
			end Select
	elseif TCode_Name = "" then			
			Set Application = Nothing	
			
	End If
	
	Rem Shutdown the connection
	Set session     = Nothing
	Connection.CloseSession("ses[0]")
	Set Connection  = Nothing

	Rem Wait a bit for the connection to be closed completely
	Wscript.Sleep 1000
	Set Application = Nothing

end	Sub




Public Sub Xls2Xlsx(ByVal fileXls)
        Dim fileXLSX
		Set filesys = CreateObject("Scripting.FileSystemObject")
		
		fileXLSX = fileXls & "X"
		If filesys.FileExists(fileXLSX) Then 
			filesys.DeleteFile(fileXLSX)
		End If
		
        Set ExcelApp = CreateObject("Excel.Application")
        Set ExcelXls = ExcelApp.Workbooks.Open(fileXls)
        ExcelXls.SaveAs fileXls & "X",51
        ExcelXls.Close        
        ExcelApp.Quit        
		
        'If filesys.FileExists(fileXLSX) Then 	
		'	filesys.DeleteFile(fileXls)			
		'End If 
		
		Set ExcelApp = Nothing	
		Set ExcelXls = Nothing
		Set filesys = Nothing
End	Sub

public sub Generate_Daywise_Report
    strWiseExport = Site_Name & "_Daywise_Effort.XLS"
	strTemp = "C:\temp\"
	
	If curMonth < 3 Then 
		tmpMonth = 1
	Else
		tmpMonth = curMonth - 2
    End If
	
	iWeekday = Weekday(Now(), vbFriday)
    LastFriday = Now - (iWeekday - 1)		   
	
    strInit = "01" & "." & tmpMonth & "." & Year(Now)
	strNow = Day(LastFriday) & "." & Month(LastFriday) & "." & Year(LastFriday)
	
	local_work_center = "385C100108"
	    	
	session.findById("wnd[0]").maximize	
	session.findById("wnd[0]/tbar[0]/okcd").text = "ZHRDAYWISE"
	session.findById("wnd[0]").sendVKey 0
	session.findById("wnd[0]/usr/ctxtS_BUKRS-LOW").text = Plant_Code	
	
	session.findById("wnd[0]/usr/ctxtS_KOSTL-LOW").text = work_center '"373C100012"'work_center '
	session.findById("wnd[0]/usr/ctxtS_KOSTL-LOW").setFocus
	session.findById("wnd[0]/usr/ctxtS_KOSTL-LOW").caretPosition = len(work_center) '10
	
	session.findById("wnd[0]").sendVKey 0
	session.findById("wnd[0]/usr/radR3").setFocus
	session.findById("wnd[0]/usr/radR3").select
	session.findById("wnd[0]/usr/ctxtS_DATE-LOW").text = strInit
	session.findById("wnd[0]/usr/ctxtS_DATE-HIGH").text = strNow
	session.findById("wnd[0]/usr/ctxtS_DATE-HIGH").setFocus
	session.findById("wnd[0]/usr/ctxtS_DATE-HIGH").caretPosition = len(strNow) '9
	session.findById("wnd[0]/tbar[1]/btn[8]").press
	session.findById("wnd[0]/tbar[1]/btn[46]").press
	session.findById("wnd[0]/tbar[1]/btn[45]").press
	session.findById("wnd[1]/usr/subSUBSCREEN_STEPLOOP:SAPLSPO5:0150/sub:SAPLSPO5:0150/radSPOPLI-SELFLAG[1,0]").select
	session.findById("wnd[1]/usr/subSUBSCREEN_STEPLOOP:SAPLSPO5:0150/sub:SAPLSPO5:0150/radSPOPLI-SELFLAG[1,0]").setFocus
	session.findById("wnd[1]/tbar[0]/btn[0]").press
	session.findById("wnd[1]/usr/ctxtDY_PATH").text = strTemp
	session.findById("wnd[1]/usr/ctxtDY_FILENAME").text = strWiseExport
	session.findById("wnd[1]/usr/ctxtDY_FILENAME").caretPosition = len(strWiseExport) '21 'BJ_Daywise_Effort.XLS
	session.findById("wnd[1]/tbar[0]/btn[0]").press	
	rem session.findById("wnd[1]/tbar[0]/btn[11]").press
	session.findById("wnd[0]/tbar[0]/btn[15]").press
	session.findById("wnd[0]/tbar[0]/btn[15]").press
	session.findById("wnd[0]/tbar[0]/btn[15]").press
	
	
	REM copy file to share drive,
    set filesys=CreateObject("Scripting.FileSystemObject")
    	
	Xls2Xlsx strTemp & strWiseExport
   
    strResultXLSX = DestPath & Site_Name & "_" & work_center & "_Daywise_Effort.XLSX"
    If filesys.FileExists(strResultXLSX) Then filesys.DeleteFile(strResultXLSX)
	
    filesys.CopyFile strTemp & strWiseExport & "X", strResultXLSX
	
	set filesys = nothing

end sub