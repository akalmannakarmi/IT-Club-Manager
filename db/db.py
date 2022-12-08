import json
import sqlite3
from datetime import datetime,timedelta

from table import Table

conn = sqlite3.connect('members.db')
cur = conn.cursor()
dbData = json.load(open("db\db.json"))

dbTable = {}

for table , tbData in dbData["tables"].items():
    dbTable[table] = Table(conn,table,tbData["FNDts"],tbData["Extra"])

def addCourse(name,startTime="06:30",breakTime="08:10",endTime="10:40",earlyEndTime="9:50",earlyEndDays=["none"]):
    if dbTable["course"].query([("Name","=",name)]):
        raise ValueError("The course already exists")
    
    dbTable["course"].insert({
        "Name":name,
        "StartTime":startTime,
        "BreakTime":breakTime,
        "EndTime":endTime,
        "EarlyEndTime":earlyEndTime
    })
    courseID = dbTable["course"].query([("Name","=",name)],["ID"])[0][0]
    
    for day in earlyEndDays:
        if not dbTable["days"].query([("Day","=",day)]):
            dbTable["days"].insert({"Day":day})
            
        dbTable["eEndDays"].insert({
            "CourseID":courseID,
            "DayID":dbTable["days"].query([("Day","=",day)],["ID"])[0][0]
        })

def addMember(name,email,password,course,interests=("None"),skills=("None"),phone="N/A",address="N/A",
    position="Member",rank="Beginer",points=0,joinDate=datetime.now(),mDeadline=datetime.now()+timedelta(days=30)):
    
    if len(name) <4:
        raise ValueError("Name Too short must be atleast 4 letters")
    elif name.isalnum():
        raise ValueError("Name can not contain numbers and special characters")
    elif len(email)<4 | email.find("@") == -1 | email.find(".")==-1:
        raise ValueError("Invalid Email")
    elif dbTable["users"].query([("Email","=",email)]):
        raise ValueError("An Account already exists with the same email")
    elif len(password) < 8:
        raise ValueError("Password must be atleast 8 characters long")
    elif not dbTable["course"].query([("Name","=",course)]):
        raise ValueError("The course does not exist. Create is first")
    else:
        dbTable["users"].insert({
            "Name":name,
            "Email":email,
            "Password":password,
            "CourseID":dbTable["course"].query([("Name","=",course)],["ID"])[0][0],
            "Phone":phone,
            "Address":address,
            "Position":position,
            "Rank":rank,
            "Points":points,
            "JoinDate":joinDate,
            "MDeadline":mDeadline
        })
        
        userID = dbTable["users"].query([("Email","=",email)],["ID"])[0][0]
        for interest in interests:
            if not dbTable["interests"].query([("Interest","=",interest)]):
                dbTable["interests"].insert({"Interest":interest})
            
            dbTable["userInterests"].insert({
                "userID":userID,
                "interestID":dbTable["interests"].query([("Interest","=",interest)],["ID"])[0][0]
            })
        
        for skill in skills:
            if not dbTable["skills"].query([("Skill","=",skill)]):
                dbTable["skills"].insert({"Skill":skill})
            
            dbTable["userSkills"].insert({
                "userID":userID,
                "skillID":dbTable["skills"].query([("Skill","=",skill)],["ID"])[0][0]
            })
        


addCourse(
    name="BCA2ndSem"
)
    
addMember(
    name="Akal Man Nakarmi2",
    email="akalnakarmi21@gmail.com",
    password="1234567890",
    course="BCA2ndSem",
    interests=["CSS","HTML","C"],
    skills=["C++","C#","Typeing"],
)