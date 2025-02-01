from datetime import *
import sqlite3
from mailer import autoMail
import json
import threading 
import time

def queryDB(): 
    rDict = {}
    conn = sqlite3.Connection("TaskTrackDB.sql")
    cur = conn.cursor() 
    cur.execute("SELECT * FROM TrackingTable")
    results = cur.fetchall() 
    for x in results: 
        result = json.loads(x[1])
        reminderDate = datetime.strptime(result["Reminder Date"],"%m/%d/%Y").strftime("%m/%d/%Y")
        currentDate = datetime.today().strftime("%m/%d/%Y")
        # Finish adding the automatic version. That will compare the current day to the reminders day.
        if currentDate == reminderDate:
            rDict[result["Name"]] = result["Created At"]
            newRDate = (datetime.strptime(reminderDate, "%m/%d/%Y") + timedelta(1)).strftime("%m/%d/%Y")
            result["Reminder Date"] = newRDate
            cur.execute("UPDATE TrackingTable SET JsonData=? WHERE TaskID=?", (json.dumps(result), x[0]))
            conn.commit()
    return rDict


def buildEmail(rDict): 
    if len(rDict) > 1: 
        emailStr = "Here is a reminder of your entries:"
        for key,value in rDict.items(): 
            test = ''.join(f"\n\n{key.title()}: Created {value}")
            emailStr += test
    elif len(rDict) == 1: 
        for key,value in rDict.items(): 
            emailStr = f"Here is a reminder for your entry \n\t{key.title()}, created: {value}"
    return emailStr

#The worker is on a background thread that is on a 24 hour sleep timer. Every 24 hours it will inform you the program is running with an email then check if its time to email your reminders. 

def worker(): 
    rDict = {}  
    while len(rDict) == 0:
        autoMail("The script is in the background")
        rDict = queryDB() 
        if len(rDict) > 0: 
            emailBody = buildEmail(rDict)
            autoMail(f"{emailBody}") 
            rDict = {}
        time.sleep(86000)

threading.Thread(target=worker).start() 

        


