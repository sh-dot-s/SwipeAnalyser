from django.conf import settings
import datetime
import nested_dict
import openpyxl
import time
import json
import os
import gc
import configparser
import pickle
import sys

dateRangeDict = nested_dict.nested_dict()
config = configparser.ConfigParser()
configPath = os.path.join(settings.BASE_DIR,"config.ini")
config.read(configPath)

def normaliseDict(items):
    for keys,values in items.items():
        if isinstance(values,datetime.datetime):
            items[keys] = values.isoformat()

        if not isinstance(values, datetime.datetime) and not isinstance(values, str):
            normaliseDict(values)
    return items

def findNextKey(dictionary,empid,key):
    i = 0
    for keys in dictionary[empid].keys():
        if str(key) == str(keys):
            i += 1
        elif i == 1:
            return str(keys)

def merge(a, b, path=None):
    if path is None: path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                pass # same leaf value
            else:
                raise Exception('Conflict at %s' % '.'.join(path + [str(key)]))
        else:
            a[key] = b[key]
    return a

def parseExcel(excelsheet, primaryEntryPoints):
    entryList =nested_dict.nested_dict()
    gateList = nested_dict.nested_dict()
    employee = nested_dict.nested_dict()
    print("Reading {}...".format(excelsheet))
    block1 = openpyxl.load_workbook(excelsheet,read_only = True)
    activeSheet = block1.get_sheet_by_name(block1.get_sheet_names()[0])
    masterDate = ""
    print("Time to load cells from XL using openpyxl")
    t = time.time()
    cells = [rows for rows in activeSheet.iter_rows(row_offset=5)]
    print(time.time()-t)
    for cell in cells:
        if any(str((cell[4].value)).startswith(substring) for substring in ["350","550","INT"]):
            # print(str((cell[4].value)))
            if cell[0].value == None:
                break
            # print(cell[0].value,cell[1].value,str((cell[4].value)),str(cell[9].value).lower(),str(cell[10].value).lower())
            dateEmp, timeEmp, empid, gate, inout =cell[0].value,cell[1].value,str((cell[4].value)),str(cell[9].value).lower(),str(cell[10].value).lower()

            try:
                formattedDate = datetime.datetime.strptime(dateEmp, "%d/%m/%Y").date()
            except:
                formattedDate = datetime.datetime.strptime(dateEmp, "%d-%m-%Y").date()
            if dateRangeDict[formattedDate] == {}:
                dateRangeDict[formattedDate] = formattedDate
            else:
                pass

            if str(gate) in primaryEntryPoints:
                if gateList[gate] == {}:
                    gateList[gate] = 0

                try:
                    cellDateTime = datetime.datetime.strptime("{} {}".format(dateEmp,timeEmp), "%d/%m/%Y %H:%M:%S")
                except:
                    cellDateTime = datetime.datetime.strptime("{} {}".format(dateEmp,timeEmp), "%d-%m-%Y %H:%M:%S")

                if cellDateTime.date() != masterDate:
                    masterDate = cellDateTime.date()
                    for keys in gateList.keys():
                        gateList[keys] +=1

                logEntry = "{} {}".format(gate,gateList[gate])

                if employee[empid][str(cellDateTime.date())][gate][logEntry] == {}:
                    entryList[gate][logEntry] = logEntry
                    employee[empid][str(cellDateTime.date())][gate][logEntry][inout] = (cellDateTime)
                else:
                    gateList[gate] += 1

                    if str(inout) in [key for key in employee[empid][str(cellDateTime.date())][gate][logEntry].keys()]:
                        logEntry = "{} {}".format(gate,gateList[gate])
                        employee[empid][str(cellDateTime.date())][gate][logEntry][inout] = (cellDateTime)
                        entryList[gate][logEntry] = logEntry
                    else:
                        employee[empid][str(cellDateTime.date())][gate][logEntry][inout] = (cellDateTime)
                        del entryList[gate][logEntry]

    return(employee)

def load_master_emp(datafile):
    global config
    gc.enable()
    now = time.time()
    i = 1
    print(datafile)
    files = datafile
    files = [files for files in files if not str(files).startswith("~$")]
    masterEmployee = nested_dict.nested_dict()
    primaryEntryPoints = ['biometric door','reception','reception 1','reception 2','main door 2','main door 1','b-1a main door 2','b-1a main door 1','biometric entry','b-1a odc front','b-1a odc exit','odc front','odc exit','b-1a reception 2','b-1a reception 1']
    reprocess = False
    dataFilePath = os.path.join(settings.MEDIA_ROOT,datafile)
    sizeF = os.path.getsize(dataFilePath)
    try:
        prevSize = config.get("size",str(datafile))
        if int(prevSize) != int(os.path.getsize(dataFilePath)):
            reprocess = True
            print("File changed.. Reprocesing...")
            config.set('size', str(datafile), str(sizeF))
            config.write(open(configPath,"w"))
    except Exception as e:
        print(e,"\nNo config item found, creating new item...")
        config.set('size', str(datafile), str(sizeF))
        config.write(open(configPath,"w"))
        reprocess = True

    if reprocess:
        if not str(datafile).startswith("~$"):
            empDictTemp = parseExcel(dataFilePath, primaryEntryPoints)
            merge(masterEmployee,empDictTemp)
            del empDictTemp
    gc.collect()
    dumpableDict = normaliseDict(masterEmployee)
    if not os.path.exists("./masterEmployee.json"):
        print("Json file missing, reprocessing the data..")
        reprocess = True

    if reprocess:
        with open("masterEmployee.json","w") as jsonFile:
            (json.dump(dumpableDict,jsonFile,indent=3))
    else:
        print("No file Change detected, loading data from json")
        with open("masterEmployee.json","r") as jsonFile:
            masterEmployee = json.load(jsonFile)
            masterEmployee =  nested_dict.nested_dict(masterEmployee)
    # print(masterEmployee)
    return(masterEmployee, normaliseDict(masterEmployee))

def shift_emp_masters():
    masterDir = os.path.join(settings.STATICFILES_DIRS[0],"masters")
    masterFile = os.path.join(masterDir,os.listdir(masterDir)[0])
    master = openpyxl.load_workbook(masterFile,read_only = True)
    activeShiftSheet = master.get_sheet_by_name("Shift Master")
    activeEmployeeSheet = master.get_sheet_by_name("Employee Master")
    shiftDict = nested_dict.nested_dict()
    irregularShifts = []
    employeeShift = {str(rows[0].value):[rows[i].value for i in range(1,len(rows))] for rows in activeEmployeeSheet.iter_rows(row_offset=1)}
    for rows in activeShiftSheet.iter_rows(row_offset=3):
        timeString = str(rows[2].value).replace(".",":").replace(" ","").split("to")
        timeFormat = "%I:%M%p"
        timeConverted = [str(datetime.datetime.strptime(temp, timeFormat).time()) for temp in timeString]
        if shiftDict[rows[0].value] == {}:
            i = 0
            shiftDict[rows[0].value][(rows[0].value+"{}".format(i))] = timeConverted
            i += 1
        else:
            shiftDict[rows[0].value][(rows[0].value+"{}".format(i))] = timeConverted
            i +=1

    for codes,entries in shiftDict.items():
        for entry in entries.keys():
            if datetime.datetime.strptime(shiftDict[codes][entry][1],"%H:%M:%S") - datetime.datetime.strptime(shiftDict[codes][entry][0],"%H:%M:%S") < datetime.timedelta(0):
                irregularShifts.append(codes)
    # print(shiftDict,employeeShift,irregularShifts)
    return (shiftDict,employeeShift,irregularShifts)

def calc_time(masterEmployee,employeeShift,irregularShifts,shiftDict,fileName):
    global dateRangeDict
    finalReport = openpyxl.Workbook()
    finalSheet = finalReport.active
    finalSheet.title = 'Master'
    if dateRangeDict == {}:
        d1, d2 = config.get("other","fromdate{}".format(fileName)),config.get("other","todate{}".format(fileName))
        d1 = datetime.datetime.strptime(d1, "%Y-%m-%d").date()
        d2 = datetime.datetime.strptime(d2, "%Y-%m-%d").date()

    else:
        dateRangeDict = [k for k in sorted(list(dateRangeDict.keys()))]
    # d1 = datetime.date(int(fromDate[0][0]), int(fromDate[0][1]), int(fromDate[0][2]))  # start date
    # d2 = datetime.date(int(fromDate[1][0]), int(fromDate[1][1]), int(fromDate[1][2]))  # end date
        d1, d2 = dateRangeDict[0], dateRangeDict[len(dateRangeDict)-1]
        config.set("other","fromdate{}".format(fileName),str(d1))
        config.set("other","todate{}".format(fileName),str(d2))
        config.write(open("config.ini","w"))

    delta = d2 - d1         # timedelta
    datesRange = []
    masterList = []
    primaryEntryPoints = ['biometric door','reception','reception 1','reception 2','main door 2','main door 1','b-1a main door 2','b-1a main door 1','biometric entry','b-1a odc front','b-1a odc exit','odc front','odc exit','b-1a reception 2','b-1a reception 1']
    datesRange.append("Emp ID")
    for i in range(delta.days + 1):
        d = str(d1 + datetime.timedelta(days=i))
        datesRange.append(d)
    finalSheet.append(datesRange)
    # masterList.append(datesRange)

    for empid,dates in masterEmployee.items():
        mess = {}
        # mess[empid] = empid
        shiftCode = employeeShift[empid][len(employeeShift[empid])-1]
        for dateR in datesRange:
            if dateR not in list(masterEmployee[empid].keys()) and dateR != "Emp ID":
                mess[dateR] = "NS"
        for date,gates in (dates.items()):
            formatteddate = datetime.datetime.strptime(date, "%Y-%m-%d")
            permOut = {}
            if shiftCode not in irregularShifts:
                inFlag,outFlag = False, False
                topGate = list(gates.keys())[0]
                bottomGate = list(gates.keys())[len(gates.keys())-1]
                topEntry = list(list(gates.values())[0].keys())[0]
                bottomEntry = list(list(gates.values())[0].keys())[len(list(gates.values())[0].keys())-1]
                inVal = masterEmployee[empid][date][topGate][topEntry]['in']
                if shiftCode == "C" and inVal != {} :
                # print(empid)
                    actualshiftin = [datetime.datetime.strptime(shiftDict[shiftCode][list(shiftDict[shiftCode].keys())[i]][0], "%H:%M:%S").time() for i in range(len(list(shiftDict[shiftCode].keys())))]
                    if any(datetime.datetime.strptime(inVal, "%Y-%m-%dT%H:%M:%S").time() < ain for ain in actualshiftin):
                        i= 0
                        while True:
                            i += 1
                            if  i > len(gates.keys())-1:
                                break
                            # print(gates.keys(),list(gates.values())[i])
                            topGate = list(gates.keys())[i]
                            topEntry = list(list(gates.values())[i].keys())[0]
                            inVal = masterEmployee[empid][date][topGate][topEntry]['in']
                            if inVal != {} and not any(datetime.datetime.strptime(inVal, "%Y-%m-%dT%H:%M:%S").time() < ain for ain in actualshiftin):
                                break
                outVal = []
                for gates in masterEmployee[empid][date].keys():
                    # print(masterEmployee[empid][date][gates].keys())
                    # for i in range(len(masterEmployee[empid][date][gates].keys())-1):
                    bottomEntry = list(masterEmployee[empid][date][gates].keys())[len(masterEmployee[empid][date][gates].keys())-1]
                    tempOut = masterEmployee[empid][date][gates][bottomEntry]['out']
                    outVal.append(masterEmployee[empid][date][gates][bottomEntry]['out'])
                    if not tempOut == {} :
                        if permOut == {}:
                            permOut = tempOut
                        if permOut != {} :
                            if datetime.datetime.strptime(tempOut, "%Y-%m-%dT%H:%M:%S") > datetime.datetime.strptime(permOut, "%Y-%m-%dT%H:%M:%S"):
                            # print(tempOut)
                                permOut = tempOut
                # outVal = masterEmployee[empid][date][bottomGate][bottomEntry]['out']
                if inVal == {}:
                    inFlag= True
                if ([outVal for outVal in outVal] == {}) or permOut == {}:
                    outFlag = True
                if not inFlag and not outFlag:
                    timeDifference = abs(datetime.datetime.strptime(permOut, "%Y-%m-%dT%H:%M:%S")-datetime.datetime.strptime(inVal, "%Y-%m-%dT%H:%M:%S"))
                if  inFlag or outFlag:
                    mess[date] = "SIOM"
                else:
                    mess[date] = timeDifference
                    # code = ruleParser(timeDifference,None,None)
                    # mess[date] += code
                    # if empid == "350055":
                    # print(empid,type(empid),timeDifference,topGate,bottomGate)
            else:
                nextDate = findNextKey(masterEmployee,empid,date)
                if nextDate != None:
                    dateCond = (datetime.datetime.strptime(nextDate, "%Y-%m-%d") - datetime.timedelta(days=1))
                    if date != str(dateCond.date()):
                        mess[date] = "SIOM"
                    else:
                        mergedTemp = merge(masterEmployee[empid][date],masterEmployee[empid][nextDate])
                        # print("Created temp dict")
                        dateShiftedDict = nested_dict.nested_dict()
                        updated = False
                        outValue,permOut = [], {}
                        actualshiftin = [datetime.datetime.strptime(shiftDict[shiftCode][list(shiftDict[shiftCode].keys())[i]][0], "%H:%M:%S").time() for i in range(len(list(shiftDict[shiftCode].keys())))]
                        actualshiftout = [datetime.datetime.strptime(shiftDict[shiftCode][list(shiftDict[shiftCode].keys())[i]][1], "%H:%M:%S").time() for i in range(len(list(shiftDict[shiftCode].keys())))]
                        inFlag,outFlag = False, False
                        for gate in mergedTemp.keys():
                            for entries in mergedTemp[gate].keys():
                                if mergedTemp[gate][entries]["in"] == {} and mergedTemp[gate][entries]["out"] == {}:
                                    pass
                                else:
                                    if mergedTemp[gate][entries]["in"] != {}:
                                        inVal = datetime.datetime.strptime(mergedTemp[gate][entries]["in"], "%Y-%m-%dT%H:%M:%S")
                                        if any(inVal.time() > ain for ain in actualshiftin) and inVal.date() == formatteddate.date():
                                            updated = True
                                            dateShiftedDict[gate][entries] = mergedTemp[gate][entries]
                                    if mergedTemp[gate][entries]["out"] != {}:
                                        outVal = datetime.datetime.strptime(mergedTemp[gate][entries]["out"], "%Y-%m-%dT%H:%M:%S")
                                        if any(outVal.time() < aout for aout in actualshiftout) and outVal.date() > formatteddate.date() :
                                            updated = True
                                            dateShiftedDict[gate][entries] = mergedTemp[gate][entries]
                        del mergedTemp
                        if updated:
                            inVal = dateShiftedDict[list(dateShiftedDict.keys())[0]][list(list(dateShiftedDict.values())[0].keys())[0]]["in"]
                            for gates in dateShiftedDict.keys():
                                bottomEntry = list(dateShiftedDict[gates].keys())[len(dateShiftedDict[gates].keys())-1]
                                tempOut = dateShiftedDict[gates][bottomEntry]['out']
                                outValue.append(dateShiftedDict[gates][bottomEntry]['out'])
                                if not tempOut == {}:
                                    permOut = tempOut
                            inFlag,outFlag = False, False
                            if inVal == {}:
                                inFlag= True
                            if ([outValue for outValue in outValue] == {}) or permOut == {}:
                                outFlag = True
                            if not inFlag and not outFlag:
                                timeDifference = abs(datetime.datetime.strptime(permOut, "%Y-%m-%dT%H:%M:%S")-datetime.datetime.strptime(inVal, "%Y-%m-%dT%H:%M:%S"))
                            if  inFlag or outFlag:
                                mess[date] = "SIOM"
                            else:
                                mess[date] = timeDifference
                                # print(empid,timeDifference,inVal,outVal)
                                # code = ruleParser(timeDifference,actualshiftin,actualshiftout)
                                # mess[date] += code
                        else:
                            mess[date] = "NS"
                else:
                    mess[date] = "NS"
        sort = {k:mess[k] for k in sorted(list(mess.keys()))}
        del mess
        sort = list(sort.values())
        sort.insert(0,empid)
        for i in range(3):
            sort.insert(i,employeeShift[empid][i])
        # print(sort)
        masterList.append(sort)
        finalSheet.append(sort)
        del sort
    finalReport.save("finalReport {}.xlsx".format(fileName))
    return(masterList, d1, d2)
