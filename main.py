import os
import math
import subprocess
import time
from pyfiglet import Figlet
import argparse
import sqlite3
from datetime import date

parser = argparse.ArgumentParser(
    prog="Command-Line Pomodoro Timer",
    description="A simple application to start a pomodoro timer in the command line"
)

parser.add_argument('-s', '--study', help="the amount of study time in minutes")
parser.add_argument('-r', '--rest', help="the amount of rest time in minutes")
parser.add_argument('-ss', '--sessions', help="the number of sessions")
parser.add_argument('-rr', '--record', action="store_true", help="enables sesssion recording")

args = parser.parse_args()

studyTime = args.study
breakTime = args.rest
sessionCount = args.sessions
recordEnable = args.record

if args.study is None or args.rest is None or args.sessions is None:
    print("You are missing 1 or more arguments. Use the -h flag for help")
    quit()

try:
    studyTime = int(studyTime)
    breakTime = int(breakTime)
    sessionCount = int(sessionCount)
except:
    print("Make sure all your arguments are whole numbers!")
    quit()

if studyTime <= 0 or breakTime <= 0 or sessionCount <= 0:
    print("Make sure all your arguments are positive numbers!")
    quit()


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

if recordEnable:
    today = date.today()
    formatted_date = today.strftime("%m/%d/%y")

    dbConn = sqlite3.connect("studylog.db")
    cursor = dbConn.cursor()
    cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS sessions (
                    date TEXT,
                    timestudied INT
            )
    ''')
    cursor.execute(f'''
            INSERT INTO sessions 
            VALUES ('{formatted_date}', {studyTime});
    ''')
    dbConn.commit()

