import os
import math
import subprocess
import time
from pyfiglet import Figlet

print("Welcome to the Command Line Pomodoro Timer App!\n")

studyTime = ""
breakTime = ""
sessionCount = ""

def getStudyTime():
    global studyTime
    studyTime = input("Enter the amount of time you would like to study for (in minutes): ")

    try:
        int(studyTime)
        studyTime = int(studyTime)
    except ValueError:
        print("Please enter an whole number value!")
        getStudyTime()
        return;

    if studyTime <= 0:
        print("Please enter a positive number!")
        getStudyTime()

    print(f"Thanks! Study time recorded to be {studyTime} minutes.\n")

def getBreakTime():
    global breakTime
    breakTime = input("Enter the amount of time you would like to rest for (in minutes): ")

    try:
        int(breakTime)
        breakTime = int(breakTime)
    except ValueError:
        print("Please enter an whole number value!")
        getBreakTime()
        return;

    if breakTime <= 0:
        print("Please enter a positive number!")
        getBreakTime()

    print(f"Thanks! Break time recorded to be {breakTime} minutes.\n")

def getSessionCount():
    global sessionCount
    sessionCount = input("Enter the number of study sessions you would like: ")

    try:
        int(sessionCount)
        sessionCount = int(sessionCount)
    except ValueError:
        print("Please enter an whole number value!")
        getSessionCount()
        return;

    if sessionCount <= 0:
        print("Please enter a positive number!")
        getSessionCount()

    print(f"Thanks! There will be {sessionCount} session(s).\n")

def isBreakLonger():
    confirmation = input("You have set the break time to be longer than the study time. Are you sure? (Y/N): ")
    print("\n")

    if confirmation == "Y":
        print("Thank you for confirming!")
    elif confirmation == "N":
        getStudyTime()
        getBreakTime() 
    else:
        print("Please either answer Y or N to confirm.") 
        isBreakLonger()

getStudyTime()
getBreakTime()
getSessionCount()

if breakTime > studyTime:
    isBreakLonger()


if studyTime <= 60: 
    studyTimeCmd = f"timer {studyTime}m"
    studySleepTime = studyTime * 60
if studyTime > 60:
    studyHours = studyTime / 60
    studyHours = math.trunc(studyHours)

    studyMinutes = studyTime % 60

    studySleepTime = (studyMinutes * 60) + (studyHours * (60 ** 2))
    if studyMinutes == 0:  
        studyTimeCmd = f"timer {studyHours}h"
    else:  
        studyTimeCmd = f"timer {studyHours}h{studyMinutes}m"
    
if breakTime <= 60: 
    breakTimeCmd = f"timer {breakTime}m"
    breakSleepTime = breakTime * 60
if breakTime > 60:
    breakHours = breakTime / 60
    breakHours = math.trunc(breakHours)

    breakMinutes = breakTime % 60

    breakSleepTime = (breakMinutes * 60) + (breakHours * (60 ** 2))
    if breakMinutes == 0:  
        studyTimeCmd = f"timer {breakHours}h"
    else:  
        studyTimeCmd = f"timer {breakHours}h{studyMinutes}m"

time.sleep(1)

for i in range(sessionCount):
    timer = subprocess.Popen(f"{studyTimeCmd} -m \"Study session {i + 1}/{sessionCount}\"", shell=True)
    time.sleep(studySleepTime)

    timer.terminate()
    os.system("clear")

    timer = subprocess.Popen(f"{breakTimeCmd} -m \"Break {i + 1}/{sessionCount}\"", shell=True)
    time.sleep(breakSleepTime)

    timer.terminate()
    os.system("clear")

f = Figlet(font='slant')
print(f.renderText('You did it!'))