import sqlite3
from tkinter import *
from tkinter.messagebox import *
from tkinter.ttk import *
from table import Table
import json

conn = sqlite3.connect('members.db')
cur = conn.cursor()
root = Tk()
root.geometry("700x500")
root.rowconfigure(0,weight=1)
root.columnconfigure(0,weight=0)
root.columnconfigure(1,weight=1)

print("The width of Tkinter window:", root.winfo_width())


class DbManager:
    def __init__(self,root):
        self.root = root
        self.root.geometry("700x500")
        self.root.title("It Club|DB Manager")
        self.root.minsize(500,500)
        
        # vars
        self.cTableName = StringVar()
        self.sTableName = StringVar()
        self.sFieldName = StringVar()
        self.afWidth = IntVar()
        self.opVar = StringVar()
        self.valueVar = StringVar()
        self.insertVars = []
        self.db = {}
        self.tables = []
        self.tableNames = []
        self.afObjs = []
        
        self.getDB()
        
        # Frames
        self.tableFrame = Frame(self.root)
        self.actionFrame = Frame(self.root)
        
        self.actionFrame.columnconfigure(0,weight=1)
        self.actionFrame.rowconfigure(0,weight=0)
        self.actionFrame.rowconfigure(1,weight=1)
        self.actionFrame.rowconfigure(2,weight=0)

        self.tableFrame.grid(column=0,row=0,sticky='nsew')
        self.actionFrame.grid(column=1,row=0,sticky='nsew')
        
        self.topAFrame = Frame(self.actionFrame,padding=10)
        self.middleAFrame = Frame(self.actionFrame,padding=10)
        self.bottomAFrame = Frame(self.actionFrame,padding=10)
        
        self.topAFrame.grid(column=0,row=0,sticky='nsew')
        self.middleAFrame.grid(column=0,row=1,sticky='nsew')
        self.bottomAFrame.grid(column=0,row=2,sticky='nsew')
        
        tFBg = Listbox(self.tableFrame)
        tFBg.place(relx=0,rely=0,relwidth=1,relheight=1)
        
        
        self.middleAFrame.columnconfigure(100,weight=1)
        self.middleAFrame.rowconfigure(100,weight=1)
        
        # aFBg = Listbox(self.actionFrame)
        # aFBg.place(relx=0,rely=0,relwidth=1,relheight=1)
        
        # taFBg = Listbox(self.topAFrame)
        # taFBg.place(relx=0,rely=0,relwidth=1,relheight=1)
        # maFBg = Listbox(self.middleAFrame)
        # maFBg.place(relx=0,rely=0,relwidth=1,relheight=1)
        # baFBg = Listbox(self.bottomAFrame)
        # baFBg.place(relx=0,rely=0,relwidth=1,relheight=1)
        
        
        self.tfDisplay()
        self.afDisplay()
        
    def getDB(self):
        dbData = json.load(open("db\db.json"))
        self.db = {}
        self.tables = []
        self.tableNames = []

        for table,tData in dbData.items():
            self.tables.append(Table(cur,table,tData["FNDts"],tData["Extra"]))
            self.tableNames.append(table)
            self.db[table] = tData

    def tfDisplay(self):
        labelTables = Label(self.tableFrame,text="Tables")
        
        selectedTable = Combobox(self.tableFrame,values=self.tableNames,textvariable=self.sTableName)
        selectedTable.set(self.tableNames[0])
        
        buttonListD = Button(self.tableFrame,text="List Data",command=lambda :self.afDisplay("List Data"))
        buttonInsertD = Button(self.tableFrame,text="Insert Data",command=lambda :self.afDisplay("Insert Data"))
        buttonRemoveD = Button(self.tableFrame,text="Remove Data",command=lambda :self.afDisplay("Remove Data"))
        buttonQueryD = Button(self.tableFrame,text="Query Data",command=lambda :self.afDisplay("Query Data"))
        buttonAddF = Button(self.tableFrame,text="Add Field",command=lambda :self.afDisplay("Add Field"))
        buttonRemoveF = Button(self.tableFrame,text="Remove Field",command=lambda :self.afDisplay("Remove Field"))
        buttonChangeF = Button(self.tableFrame,text="Change Field",command=lambda :self.afDisplay("Change Field"))
        buttonDeleteT = Button(self.tableFrame,text="Delete Table",command=lambda :self.afDisplay("Delete Table"))
        
        entryCreateT = Entry(self.tableFrame,textvariable=self.cTableName)
        buttonCreateT = Button(self.tableFrame,text="Create table",command=lambda :self.afDisplay("Create Table"))
        
        labelTables.pack(pady=10)
        selectedTable.pack(padx=10,pady=5)
        
        buttonListD.pack(padx=10,pady=5)
        buttonInsertD.pack(padx=10,pady=5)
        buttonRemoveD.pack(padx=10,pady=5)
        buttonQueryD.pack(padx=10,pady=5)
        buttonAddF.pack(padx=10,pady=5)
        buttonChangeF.pack(padx=10,pady=5)
        buttonRemoveF.pack(padx=10,pady=5)
        buttonDeleteT.pack(padx=10,pady=5)
        
        entryCreateT.pack(padx=10,pady=5)
        buttonCreateT.pack(padx=10,pady=5)

    def afDisplay(self,scene="None"):
        for obj in self.afObjs:
            obj.destroy()

        if scene == "Create Table":
            self.createTable()
        elif scene == "List Data":
            self.listData()
        elif scene == "Insert Data":
            self.insertData()
        elif scene == "Remove Data":
            self.removeData()
        elif scene == "Query Data":
            self.queryData()
            
            
    def createTable(self):
        lableTbName = Label(self.topAFrame,text=self.cTableName.get())
        lableFNDts = Label(self.topAFrame,text="Fields and Data types")
        self.afObjs.append(lableTbName)
        self.afObjs.append(lableFNDts)
        lableTbName.pack()
        lableFNDts.pack()
    
    def listData(self):
        lableTbName = Label(self.topAFrame,text="Selected Table:"+self.sTableName.get())
        self.afObjs.append(lableTbName)
        lableTbName.pack()
        
        dataFrame = Frame(self.middleAFrame,padding=10)
        dataFrame.grid(column=0,row=2,columnspan=101,rowspan=100,sticky='nsew')
        
        scroll = Scrollbar(dataFrame) 
        scrollx = Scrollbar(dataFrame,orient='horizontal') 
        list = Listbox(dataFrame,yscrollcommand=scroll.set,xscrollcommand=scrollx.set,font='Courier') 
        self.afObjs.append(scroll)
        self.afObjs.append(scrollx)
        self.afObjs.append(list)
        scroll.config(command = list.yview)
        scrollx.config(command = list.xview)
        
        fields=""
        for field in self.db[self.sTableName.get()]["FNDts"]:
            fields += field+" "*(22-len(field))
        list.insert(END,fields) 
        
        table = Table(cur,self.sTableName.get(),self.db[self.sTableName.get()]["FNDts"],self.db[self.sTableName.get()]["Extra"])
        data = table.query()
        for da in data: 
            record = ""
            for d in da:
                record+=str(d)+" "*(22-len(str(d)))
            list.insert(END,record) 
                    
        
        scroll.pack(side = RIGHT, fill = Y) 
        scrollx.pack(side = BOTTOM, fill = X) 
        list.pack(side=TOP,fill=BOTH,padx=10,pady=10,expand=1)
        # list.place(relx=.04,y=50,relwidth=.9,relheight=.8)
    
    def insertData(self):
        # Set the Top frame
        lableTbName = Label(self.topAFrame,text="Selected Table:"+self.sTableName.get())
        self.afObjs.append(lableTbName)
        lableTbName.pack()
        
        #Set the Main Frame (Middle Frame)
        self.insertVars= []
        row = column = 0
        for field,dataType in self.db[self.sTableName.get()]["FNDts"].items():
            if field == "ID":
                continue
            if dataType.find("INTEGER") != -1:
                label_ = Label(self.middleAFrame,text=field+":Integer")
                entryData = IntVar()
            else:
                label_ = Label(self.middleAFrame,text=field+":String")
                entryData = StringVar()
            
            entry_ = Entry(self.middleAFrame,textvariable=entryData)
            self.insertVars.append(entryData)
            self.afObjs.append(label_)
            self.afObjs.append(entry_)
            
            label_.grid(column=column,row=row,padx=5,pady=10)
            column +=1
            entry_.grid(column=column,row=row,padx=5,pady=10)
            column +=1
            if column >3:
                column=0
                row+=2
        
        # Set the Bottom Frame
        insertButton = Button(self.bottomAFrame,text="Insert",command=self.insert)
        self.afObjs.append(insertButton)
        insertButton.pack(side="right")
        
    def insert(self):
        table = Table(cur,self.sTableName.get(),self.db[self.sTableName.get()]["FNDts"],self.db[self.sTableName.get()]["Extra"])
        i = 0
        fieldNValues={}
        for field in self.db[self.sTableName.get()]["FNDts"]:
            if field == "ID":
                continue
            fieldNValues[field] = self.insertVars[i].get()
            i+=1
        
        try:
            table.insert(fieldNValues)
            conn.commit()
            showinfo("Inserted",f"Inserted Data: {fieldNValues}")
        except BaseException as e :
            showerror("Failed To insert",f"Tried to Insert Data: {fieldNValues} \n Got Error: {e}")
        
    def removeData(self):
        # Set the Top frame
        lableTbName = Label(self.topAFrame,text="Selected Table:"+self.sTableName.get())
        self.afObjs.append(lableTbName)
        lableTbName.pack()
        
        # Set the Middle Frame(Main)
        
        fields = ["Not Selected"]+ [ field for field in self.db[self.sTableName.get()]["FNDts"]]
        
        lablelField = Label(self.middleAFrame,text="Field")
        selectedField = Combobox(self.middleAFrame,values=fields,textvariable=self.sFieldName)
        selectedField.set(fields[0])
        lablelOp = Label(self.middleAFrame,text="Operator")
        operatorEntry =  Entry(self.middleAFrame,textvariable=self.opVar)
        lablelValue = Label(self.middleAFrame,text="Value")
        valueEntry =  Entry(self.middleAFrame,textvariable=self.valueVar)
        self.afObjs.append(lablelField)
        self.afObjs.append(selectedField)
        self.afObjs.append(lablelOp)
        self.afObjs.append(operatorEntry)
        self.afObjs.append(lablelValue)
        self.afObjs.append(valueEntry)
        
        lablelField.grid(column=0,row=0,padx=5,pady=5)
        selectedField.grid(column=0,row=1,padx=5,pady=5)
        lablelOp.grid(column=1,row=0,padx=5,pady=5)
        operatorEntry.grid(column=1,row=1,padx=5,pady=5)
        lablelValue.grid(column=2,row=0,padx=5,pady=5)
        valueEntry.grid(column=2,row=1,padx=5,pady=5)
        
        # Set the Bottom Frame
        removeButton = Button(self.bottomAFrame,text="Remove",command=self.remove)
        self.afObjs.append(removeButton)
        removeButton.pack(side="right")
        
    
    def remove(self):
        table = Table(cur,self.sTableName.get(),self.db[self.sTableName.get()]["FNDts"],self.db[self.sTableName.get()]["Extra"])
        
        
        try:
            table.remove(self.valueVar.get(),self.sFieldName.get(),self.opVar.get())
            conn.commit()
            showinfo("Removed",f"Removed Data Where: {self.sFieldName.get()}{self.opVar.get()}{self.valueVar.get()}")
        except BaseException as e :
            showerror("Failed To remove",f"Tried to Remove Where: {self.sFieldName.get()}{self.opVar.get()}{self.valueVar.get()} \n Got Error: {e}")
        
    def queryData(self):
        # Set the Top frame
        lableTbName = Label(self.topAFrame,text="Selected Table:"+self.sTableName.get())
        self.afObjs.append(lableTbName)
        lableTbName.pack()
        
        # Set the Middle Frame(Main)
        
        fields = ["Not Selected"]+ [ field for field in self.db[self.sTableName.get()]["FNDts"]]
        
        lablelField = Label(self.middleAFrame,text="Field")
        selectedField = Combobox(self.middleAFrame,values=fields,textvariable=self.sFieldName)
        selectedField.set(fields[0])
        lablelOp = Label(self.middleAFrame,text="Operator")
        operatorEntry =  Entry(self.middleAFrame,textvariable=self.opVar)
        lablelValue = Label(self.middleAFrame,text="Value")
        valueEntry =  Entry(self.middleAFrame,textvariable=self.valueVar)
        self.afObjs.append(lablelField)
        self.afObjs.append(selectedField)
        self.afObjs.append(lablelOp)
        self.afObjs.append(operatorEntry)
        self.afObjs.append(lablelValue)
        self.afObjs.append(valueEntry)
        
        lablelField.grid(column=0,row=0,padx=5,pady=5)
        selectedField.grid(column=0,row=1,padx=5,pady=5)
        lablelOp.grid(column=1,row=0,padx=5,pady=5)
        operatorEntry.grid(column=1,row=1,padx=5,pady=5)
        lablelValue.grid(column=2,row=0,padx=5,pady=5)
        valueEntry.grid(column=2,row=1,padx=5,pady=5)
        
        # TO view Data
        dataFrame = Frame(self.middleAFrame,padding=10)
        dataFrame.grid(column=0,row=2,columnspan=101,rowspan=100,sticky='nsew')
        scroll = Scrollbar(dataFrame) 
        scrollx = Scrollbar(dataFrame,orient='horizontal') 
        self.queryList = Listbox(dataFrame,yscrollcommand=scroll.set,xscrollcommand=scrollx.set,font='Courier') 
        self.afObjs.append(scroll)
        self.afObjs.append(scrollx)
        self.afObjs.append(self.queryList)
        scroll.config(command = self.queryList.yview)
        scrollx.config(command = self.queryList.xview)
        scroll.pack(side = RIGHT, fill = Y) 
        scrollx.pack(side = BOTTOM, fill = X) 
        self.queryList.pack(side=TOP,fill=BOTH,padx=10,pady=10,expand=1)
        
        # Set the Bottom Frame
        queryButton = Button(self.bottomAFrame,text="Query",command=self.query)
        self.afObjs.append(queryButton)
        queryButton.pack(side="right")
        
    def query(self):
        self.queryList.delete(0,END)
        fields=""
        for field in self.db[self.sTableName.get()]["FNDts"]:
            fields += field+" "*(22-len(field))
        self.queryList.insert(END,fields) 
        
        table = Table(cur,self.sTableName.get(),self.db[self.sTableName.get()]["FNDts"],self.db[self.sTableName.get()]["Extra"])
        try:
            data = table.query([(self.sFieldName.get(),self.opVar.get(),self.valueVar.get())])
            # showinfo("Query",f"Queried Data Where: {self.sFieldName.get()}{self.opVar.get()}{self.valueVar.get()}")
        except BaseException as e :
            showerror("Failed To Query",f"Tried to Query Where: {self.sFieldName.get()}{self.opVar.get()}{self.valueVar.get()} \n Got Error: {e}")
        
        for da in data: 
            record = ""
            for d in da:
                record+=str(d)+" "*(22-len(str(d)))
            self.queryList.insert(END,record) 

def run():
    dbManager = DbManager(root)

if __name__ == "__main__":
    run()
    root.mainloop()