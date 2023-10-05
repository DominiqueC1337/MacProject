import requests
import re  # Regex

API_URL = "https://ikarus.webuntis.com/WebUntis/monitor/substitution/data?school=hh5918"
classname = ""


def getDataForDate(date, classname):
    # Macht einen Request zu Untis mit dem angefragten Datum und gibt formatierte Daten zurück
    # print("Getting data for {}".format(date))
    # Achtung beim ändern, muss der [data index] angepasst werden
    requirements = {
        "formatName": "FgarV5344HGhuasdfz",
        "schoolName": "hh5918",
        "date": date,
        "dateOffset": 0,
        "strikethrough": True,
        "mergeBlocks": True,
        "showOnlyFutureSub": True,
        "showBreakSupervisions": False,
        "showTeacher": False,
        "showClass": True,
        "showHour": True,
        "showInfo": True,
        "showRoom": True,
        "showSubject": False,
        "groupBy": 1,
        "hideAbsent": False,
        "departmentIds": [],
        "departmentElementType": -1,
        "hideCancelWithSubstitution": False,
        "hideCancelCausedByEvent": False,
        "showTime": True,
        "showSubstText": True,
        "showAbsentElements": [],
        "showAffectedElements": [],
        "showUnitTime": False,
        "showMessages": False,
        "showStudentgroup": False,
        "enableSubstitutionFrom": False,
        "showSubstitutionFrom": 0,
        "showTeacherOnEvent": False,
        "showAbsentTeacher": False,
        "strikethroughAbsentTeacher": False,
        "activityTypeIds": [],
        "showEvent": False,
        "showCancel": True,
        "showOnlyCancel": False,
        "showSubstTypeColor": False,
        "showExamSupervision": False,
        "showUnheraldedExams": False
    }
    responseData = requests.post(API_URL, json=requirements).json()
    return filterData(responseData, classname)

def filterData(data, classname):
    # filtert Daten und organisiert diese
    payload = data["payload"]
    outData = {}
    outData["last_update"] = payload["lastUpdate"]
    outData["week_day"] = payload["weekDay"]
    outData["date"] = payload["date"]
    outData["results"] = []
    outData["next_day"] = payload["nextDate"]

    filterByClass = classname != None and classname != ""

    for entry in payload["rows"]:
        # jeder "entry" ist eine Vertretungseinheit
        # {'data': ['3', '09:30-10:15', 'AV2c', '86', '', 'in Mitbetreuung'], 'cssClasses': [], 'cellClasses': {}, 'group': 'AV2c'}

        if entry["group"] == classname or not filterByClass:
            entryData = {}
            entryData["class"] = striphtml(entry["group"])
            # [data index] start
            entryData["hour"] = striphtml(entry["data"][0])
            entryData["time"] = striphtml(entry["data"][1])
            entryData["room"] = striphtml(entry["data"][3])
            entryData["info"] = striphtml(entry["data"][5])
            # [data index] end
            # {'class': 'AV2c', 'hour': '3', 'time': '09:30-10:15', 'room': '86', 'info': 'in Mitbetreuung'}
            outData["results"].append(entryData)
    return outData

def striphtml(data):
    # löscht alle HTML-Tags
    p = re.compile(r'<.*?>')
    return p.sub('', data)
