import json
from datetime import * 
from argparse import * 
import sqlite3 
from mailer import autoMail


parser = ArgumentParser() 
parser.add_argument("-add", help="adds a new task",type=str)
parser.add_argument("-list", help="lists all current tasks", action="store_true")
parser.add_argument("-udesc", help="updates the description of a task", type=int)
parser.add_argument("-ustatus",help="updates the status of a task", type=int)
parser.add_argument("-remove",help="removes a task", action="store_true")
parser.add_argument("-removeall",help="completely clears your tasks", action="store_true")
parser.add_argument("-listtd", help="lists all tasks that are marked todo", action="store_true")
parser.add_argument("-listip", help="lists all tasks that are marked in-progress", action="store_true")
parser.add_argument("-setreminders",help="set the frequency of the reminders", action="store_true")
args = parser.parse_args() 

class TaskTracker: 
    def __init__(self): 
        self.DB = DBConnection() 
    def addTask(self,taskName): 
        taskName = taskName.lower().rstrip() +'.json'
        taskDescription = input("Enter a description of the task: ")
        dateCreated = datetime.today()
        taskStatus = self.setTaskStatus()
        currentTask = self.createProperties(taskName.rstrip(".json"),taskDescription,taskStatus,dateCreated)
        self.DB.addToDB(json.dumps(currentTask))

    def setTaskStatus(self): 
        try: 
            userInput = int(input("Enter the task's status (1= todo / 2= in-progress / 3= done): "))
            if userInput == 1:  
                status = 'todo'
            elif userInput == 2: 
                status = "in-progress"
            elif userInput == 3: 
                status = "done"
            else: 
                status = 'todo'
        except Exception as e: 
            print(e)
            print("Enter an integer")
        return status  
                            
    def createProperties(self,taskName,description,status,dateCreated,dateUpdated=None): 
        currentTask = {}
        currentTask["Name"] = taskName
        currentTask["Description"] = description
        currentTask["status"] = status 
        currentTask["Created At"] = dateCreated.strftime("%m/%d/%Y") 
        currentTask["Reminder Date"] = dateCreated.strftime("%m/%d/%Y") #(dateCreated + timedelta(1)).strftime("%m/%d/%Y")
        currentTask["Updated At"] = dateUpdated
        return currentTask 

    def deleteTask(self,remAll=False): 
        if remAll == True: 
            resultList = self.DB.getEntries() 
            for result in resultList: 
                self.DB.delEntry(result[0])
        else: 
            self.taskList()
            try: 
                userInput = int(input("Enter the ID of the task you'd like to delete: "))
                resultList = self.DB.getEntries() 
                for result in resultList: 
                    if result[0] == userInput: 
                        self.DB.delEntry(userInput)
            except Exception as e: 
                print(e)
                print("Please enter an integer!")


    def updateTaskStatus(self): 
        #get the task json result. Create a copy of the result with the updated status. 
        #Then put the copied task back into the spot of the original task replacing it.
        self.taskList()
        try: 
            updatedDate = datetime.today().strftime("%b %d %Y")
            userInput = int(input("Enter the ID of the task you'd like to update: "))
            
        except Exception as e: 
            print(e)
            print("Please enter an integer!")

    def updateTaskDesc(self):
        #get the task json result. Create a copy of the result with the updated description. 
        #Then put the copied task back into the spot of the original task replacing it. 
        self.taskList() 
        try: 
            updatedDate = datetime.today().strftime("%b %d %Y")
            userInput = int(input("Enter the ID of the task you'd like to update: "))
            result = self.DB.updateTaskStatus()
            taskJson = json.loads(result[1])
            taskJson["Description"] = input("Enter your new description:\n")
        except Exception as e: 
            print(f"{e}, Please enter an integer!")

                      
    def taskList(self): 
        resultList = self.DB.getEntries() 
        for result in resultList: 
            task = json.loads(result[1])
            print(f'''Task: {task["Name"].title()} \n\tID: {result[0]} \n\tDescription: {task["Description"]} \n\tStatus: {task["status"]} \n\tCreated: {task["Created At"]}''')

    def taskListTodo(self): 
        resultList = self.DB.getEntries() 
        for result in resultList: 
            task = json.loads(result[1])
            if task["status"].lower() == "todo":
                print(f"Task: {task["Name"].title()} \n\tID: {result[0]} \n\tDescription: {task["Description"]} \n\tStatus: {task["status"]} \n\tCreated: {task["Created At"]}")

    def taskListInProgress(self): 
        resultList = self.DB.getEntries() 
        for result in resultList: 
            task = json.loads(result[1])
            if task["status"].lower() == "in-progress":
                print(f"Task: {task["Name"].title()} \n\tID: {result[0]} \n\tDescription: {task["Description"]} \n\tStatus: {task["status"]} \n\tCreated: {task["Created At"]}") 
    
    def taskListDone(self): 
        pass 

class DBConnection: 
    def __init__(self): 
        self.conn = sqlite3.connect("TaskTrackDB.sql")
        self.cur = self.conn.cursor() 
    def createTable(self): 
        self.cur.execute("CREATE TABLE IF NOT EXISTS TrackingTable (TaskID Integer Primary Key NOT NULL, JsonData TEXT)")
    def addToDB(self,jsonObject): 
        self.cur.execute("INSERT INTO TrackingTable (JsonData) VALUES (?)", (jsonObject,))
        self.conn.commit()
    def getEntries(self):
        results = self.cur.execute("SELECT * from TrackingTable")
        testing = results.fetchall()
        return testing
    def delEntry(self,taskID):
        self.cur.execute("DELETE FROM TrackingTable WHERE TaskID == (?)", (taskID,))
        self.conn.commit()
    def updateTaskStatus(self,taskID): 
        result = self.cur.execute("SELECT FROM TrackingTable WHERE TaskID == (?)", (taskID,))
        return result

def main(): 
    FirstTask = TaskTracker()
    userDB = DBConnection()
    userDB.createTable()
    if args.list: 
        FirstTask.taskList()
    if args.add != None: 
        FirstTask.addTask(args.add)
    if args.remove: 
        FirstTask.deleteTask()
    if args.listtd:
        FirstTask.taskListTodo()
    if args.listip: 
        FirstTask.taskListInProgress() 
    if args.removeall:
        FirstTask.deleteTask(True)
    if args.setreminders:
        secondsFrequency = int(input("Enter the frequency in days: "))
        daysFrequency = (secondsFrequency*60*60*24)
        print(daysFrequency)

main()
