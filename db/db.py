import json
import sqlite3
from datetime import datetime,timedelta
from time import time
from termcolor import cprint

from .table import Table


dbData = json.load(open("db\db.json"))
conn = sqlite3.connect('members.db',check_same_thread=False)
cur = conn.cursor()

dbTable = {}

for table , tbData in dbData.items():
    dbTable[table] = Table(cur,table,dbData)


def addCourse(name,startTime="06:30",breakTime="08:10",endTime="10:40",earlyEndTime="9:50",earlyEndDays=["none"],allData=None):
    if allData:
        name = allData['name']
        startTime = allData.get('startTime','06:30')
        breakTime = allData.get('breakTime','08:10')
        endTime = allData.get('endTime','10:40')
        earlyEndTime = allData.get('earlyEndTime','9:50')
        earlyEndDays = allData.get('earlyEndDays',["none"])
    
    # Course Already exists
    if dbTable['course'].query([("Name","=",name)]):
        raise ValueError("The course already exists")
    
    dbTable['course'].insert({
        "Name":name,
        "StartTime":startTime,
        "BreakTime":breakTime,
        "EndTime":endTime,
        "EarlyEndTime":earlyEndTime
    })
    courseID = dbTable['course'].query([("Name","=",name)],["ID"])[0][0]
    
    for day in earlyEndDays:
        if not dbTable['days'].query([("Day","=",day)]):
            dbTable['days'].insert({"Day":day})
            
        dbTable['eEndDays'].insert({
            "CourseID":courseID,
            "DayID":dbTable['days'].query([("Day","=",day)],["ID"])[0][0]
        })
        
    return conn.commit

def addMember(name,email,password,course,interests=("None"),skills=("None"),phone="N/A",address="N/A",
    position="Member",rank="Beginer",points=0,joinDate=datetime.now(),mDeadline=datetime.now()+timedelta(days=30),allData=None):

    if allData:
        name = allData['name']
        email = allData['email']
        password = allData['password']
        course = allData['course']
        interests = allData.get('interests',("None"))
        skills = allData.get('skills',("None"))
        phone = allData.get('phone','N/A')
        address = allData.get('address','N/A')
        position = allData.get('position','Member')
        rank = allData.get('rank','Beginer')
        points = allData.get('points',0)
        joinDate = allData.get('joinDate',datetime.now())
        mDeadline = allData.get('mDeadline',datetime.now()+timedelta(days=30))
    
    # Doing required queries
    course = dbTable['course'].query([("Name","=",course)],['ID'])
    
    # Conditions for valid Data
    if len(name) <4:
        raise ValueError("Name Too short must be atleast 4 letters")
    elif name.isalnum():
        raise ValueError("Name can not contain numbers and special characters")
    elif len(email)<4 | email.find("@") == -1 | email.find(".")==-1:
        raise ValueError("Invalid Email")
    elif dbTable['users'].query([("Email","=",email)]):
        raise ValueError("An Account already exists with the same email")
    elif len(password) < 8:
        raise ValueError("Password must be atleast 8 characters long")
    elif not course:
        raise ValueError("The course does not exist. Create is first")
    
    # Inserting 
    dbTable['users'].insert({
        "Name":name,
        "Email":email,
        "Password":password,
        "CourseID":course[0][0],
        "Phone":phone,
        "Address":address,
        "Position":position,
        "Rank":rank,
        "Points":points,
        "JoinDate":joinDate,
        "MDeadline":mDeadline
    })
    
    
    # Adding Interests and skills
    userID = dbTable['users'].query([("Email","=",email)],["ID"])[0][0]
    if type(interests)==str:
        interests=interests.split(',')
    for interest in interests:
        interest = interest.strip()
        if not dbTable['interests'].query([("Interest","=",interest)]):
            dbTable['interests'].insert({"Interest":interest})
        
        dbTable['userInterests'].insert({
            "userID":userID,
            "interestID":dbTable['interests'].query([("Interest","=",interest)],["ID"])[0][0]
        })
    if type(skills)==str:
        skills=skills.split(',')
    for skill in skills:
        skill = skill.strip()
        if not dbTable['skills'].query([("Skill","=",skill)]):
            dbTable['skills'].insert({"Skill":skill})
        
        dbTable['userSkills'].insert({
            "userID":userID,
            "skillID":dbTable['skills'].query([("Skill","=",skill)],["ID"])[0][0]
        })
        
    return conn.commit
    
    
def getMember(getFields,email=None,name=None):
    if email:
        return dbTable['users'].query([('email','=',email)],getFields)
    if name:
        return dbTable['users'].query([('name','=',name)],getFields)
    raise SyntaxError("Must pass a value to getMember")

def getMembers(conditions=None,fields=None,orderby=''):
    result = []
    # For contition in another table
    for field,op,value in conditions:
        if field == 'Course':
            IDs = dbTable["course"].query([("Name",op,value)],['ID'])
            Id = listify(IDs)
            return getMembers([("CourseID","IN",Id)],fields)
        elif field == 'Interest':
            IDs = dbTable["interests"].query([("Interest",op,value)],['ID'])
            Id = listify(IDs)
            UIDs = dbTable["userInterests"].query([("InterestID",'IN',Id)],["UserID"])
            UId = listify(UIDs)
            return getMembers([("ID","IN",UId)],fields)
        elif field == 'Skill':
            IDs = dbTable["skills"].query([("Skill",op,value)],['ID'])
            Id = listify(IDs)
            UIDs = dbTable["userSkills"].query([("SkillID",'IN',Id)],["UserID"])
            UId = listify(UIDs)
            return getMembers([("ID","IN",UId)],fields)
    # Store the fields to get when quering
    qFields=['ID']
    for field in fields:
        for field_ in dbTable['users'].fND:
            if field == 'Interests' or field =='Course' or field =='Skills' or field in qFields:
                break
            elif field == field_ :
                qFields.append(field)
    qData = dbTable['users'].query(conditions,qFields)
    for row in qData:
        t = []
        for field in fields:
            val = "Invalid"
            if field == 'Interests':
                interestIDs =dbTable["userInterests"].query([('UserID','=',row[0])],['InterestID'])
                interestIDs = listify(interestIDs)
                vals = dbTable["interests"].query([('ID','IN',interestIDs)],['Interest'])
                val = ', '.join(listify(vals))
            elif field == 'Skills':
                skillIDs =dbTable["userSkills"].query([('UserID','=',row[0])],['SkillID'])
                skillIDs = listify(skillIDs)
                vals = dbTable["skills"].query([('ID','IN',skillIDs)],['Skill'])
                val = ', '.join(listify(vals))
            elif field == 'Course':
                courseID =dbTable["users"].query([('ID','=',row[0])],['CourseID'])
                vals = dbTable["course"].query([('ID','=',courseID[0][0])],['Name'])
                val = ', '.join(listify(vals))
            else:
                for i in range(0,len(qFields)):
                    if field == qFields[i]:
                        val = row[i]
            t.append(val)
        result.append(t)   
    return result

def changeMember(email,fieldNValues):
    userID = dbTable["users"].query([("Email","=",email)],["ID"])[0][0]
    print(fieldNValues)
    for field,value in fieldNValues.items(multi=False):
        if field == "0password":
            if value:
                dbTable["users"].update([("Password",value)],[("ID","=",userID)])
        elif field == "course":
            courseID = dbTable["course"].query([('Name','=',value)],['ID'])[0][0]
            dbTable["users"].update([("CourseID",courseID)],[("ID","=",userID)])
        elif field == "interests":
            dbTable["userInterests"].remove(userID,"UserID",'=')
            interests=value.split(",")
            for interest in interests:
                interest = interest.strip()
                if not dbTable['interests'].query([("Interest","=",interest)]):
                    dbTable['interests'].insert({"Interest":interest})
        
                dbTable['userInterests'].insert({
                    "userID":userID,
                    "interestID":dbTable['interests'].query([("Interest","=",interest)],["ID"])[0][0]
                })
        elif field == "skills":
            skills=value.split(',')
            for skill in skills:
                skill = skill.strip()
                if not dbTable['skills'].query([("Skill","=",skill)]):
                    dbTable['skills'].insert({"Skill":skill})
                
                dbTable['userSkills'].insert({
                    "userID":userID,
                    "skillID":dbTable['skills'].query([("Skill","=",skill)],["ID"])[0][0]
                })
        else:    
            dbTable["users"].update([(field,value)],[("ID","=",userID)])
    
    return conn.commit

def getInterests(conditions=None,fields=None):
    return dbTable['interests'].query(conditions,fields)

def getCourses(conditions=None,fields=None):
    return dbTable['course'].query(conditions,fields)

def listify(data):
    result = []
    for val in data:
        result.append(val[0])
    return result

try:
    commit=addCourse(name="BCA2")
    commit()
except Exception as e:
    cprint(f"Add course BCA2 Error:{e}",'yellow')
    
# addMember(
#     name="Akal Man Nakarmi2",
#     email="akalnakarmi21@gmail.com",
#     password="1234567890",
#     course="BCA2ndSem",
#     interests=["CSS","HTML","C"],
#     skills=["C++","C#","Typeing"],
# )