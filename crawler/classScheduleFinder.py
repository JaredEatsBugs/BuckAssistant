from __future__  import division, unicode_literals
import codecs
from bs4 import BeautifulSoup
import sys
import re
import json

def readFile(file_name, output_file):
    file = codecs.open(file_name, 'r', 'utf-8')
    document = BeautifulSoup(file.read()).get_text()
    document_file = open(output_file, 'w')
    document_file.write(document)

def getClassList(file_name):
    ##file = open(file_name, 'r')
    file = open('crawler/classScheduleHeader.txt')
    class_list = {}
    start = False
    while True:
        line = file.readline()
        if line:
            if 'Catalog Number' in line:
                start = True
            if 'Location' in line:
                break
            if start:
                schedule_options = {}
                line = "CSE " + line
                class_list.update({line : schedule_options})
        else :
            break
    file.close()
    return class_list
    
def parseTime(time, session):
    parsed_time = [0,[0,0,0,0,0], (0,0)]
    if "Session 1" in session:
        parsed_time[0] = -1
    elif "Session 2" in session:
        parsed_time[0] = 1
    weekday = [0,0,0,0,0]
    if "ARR" in time:
        return parsed_time
    if "M" in time:
        weekday[0] = 1
    if "T" in time:
        weekday[1] = 1
    if "W" in time:
        weekday[2] = 1
    if "TR" in time:
        weekday[3] = 1
    if "F" in time:
        weekday[4] = 1
    parsed_time[1] = weekday

    interval = time[-14:]
    start_time = interval[:2] + interval[3:5]
    end_time = interval[8:10] + interval[11:13]

    parsed_time[2] = (start_time,end_time)
    return parsed_time

def getClassInfoBLock(class_name, file_name):
    file = open('crawler/' + file_name, 'r')
    schedule_options = {}
    block = False
    while True:
        line = file.readline()
        if line:
            if class_name in line:
                block = True
            if re.search(r"(CSE ){1}\d{4}((.0){1}\d{1})*", line):
                next_name = re.search(r"(CSE ){1}\d{4}((.0){1}\d{1})*", line).group(0)
                if class_name != next_name:
                    break
            if block:
                while re.search(r"\d{5}",line):
                    schedule_option = {}
                    section_name = re.search(r"\d{5}",line).group(0)
                    schedule_option.update({'Class Number': section_name})
                    component = file.readline()
                    schedule_option.update({'Component' : component})
                    location = file.readline()
                    schedule_option.update({'Location' : location})
                    times = file.readline()
                    insturctor = file.readline()
                    session = file.readline()
                    topic = file.readline()
                    time = parseTime(times,session)
                    schedule_option.update({'Time': time})
                    schedule_option.update({"Instructor" : insturctor})
                    schedule_option.update({"Topic" : topic})

                    if section_name in schedule_options:
                        old_time = schedule_options[section_name]['Time']
                        old_time[1][0] = old_time[1][0] + time[1][0]
                        old_time[1][1] = old_time[1][1] + time[1][1]
                        old_time[1][2] = old_time[1][2] + time[1][2]
                        old_time[1][3] = old_time[1][3] + time[1][3]
                        old_time[1][4] = old_time[1][4] + time[1][4]
                        

                    schedule_options.update({section_name : schedule_option})
                    line = file.readline()
        else:
            break
    file.close()
    return schedule_options

def AllClassSchedule(file_name):
    AllClassSchedule = {}
    class_list = getClassList(file_name)

    for class_name in class_list:
        AllClassSchedule.update({class_name  : getClassInfoBLock(class_name, file_name)})
    
    return AllClassSchedule

def saveAllClassSchedule(file_name):
    ClassesSchedules = AllClassSchedule(file_name)
    json_file = open('CSEClassSchedules.json', 'w')
    json.dump(ClassesSchedules, json_file)


    
def loadAllClassSchedule():
    schedule_file = open('CSEClassSchedules.json', 'r')
    ClassesSchedules = json.load(schedule_file)
    return ClassesSchedules

def queryClassSchedule(class_name):
    ClassesSchedules = loadAllClassSchedule()
    queriedClassSchedule = ClassesSchedules[class_name] 
    return queriedClassSchedule


##saveAllClassSchedule('classSchedule.txt')

schedule = getClassInfoBLock("CSE 1110", "classSchedule.txt")
print(schedule)




    
            



            
