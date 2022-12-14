from termcolor import cprint

class Table:
    def __init__(self,cur,name,fieldNTypes,extra=None,displayF=cprint,dColor='green',eDColor='yellow'):
        self.cur = cur
        self.name = name
        self.fND = {}
        self.display = displayF
        self.color = dColor
        self.eColor = eDColor
        self.create(fieldNTypes,extra)
    
    def create(self,fieldNTypes,extra,show=True):
        if self.name in fieldNTypes:
            (fieldNTypes,extra) = self.destructure(fieldNTypes[self.name])
        
        c = f"CREATE TABLE {self.name} ("
        for field,type in fieldNTypes.items():
            self.fND[field]=type
            c += f"{field} {type},"
        if extra:
            c += extra
        else:
            c = c[:-1]
        c += ")"
        
        if show:
            self.display(f"Creating Table:{self.name} \nCommand:{c}",self.color)
            
        try:
            self.cur.execute(c)
            if show:
                self.display("Result: Success",self.color)
        except BaseException as e:
            if show:
                self.display(f"Result: Failed \tError:{e}",self.eColor)


    def insert(self,fieldNValues,show=True):
        fields = "("
        sValues = "("
        values = []
        for field,value in fieldNValues.items():
            fields += field + ","
            sValues += "?,"
            values.append(value)
        fields = fields[:-1] + ")"
        sValues = sValues[:-1] + ")"
        
        c = f"INSERT INTO {self.name} {fields} VALUES {sValues}"
        
        if show:
            self.display(f"Insert to Table:{self.name} \nCommand:{c}\tValues:{values}",self.color)
            
        try:
            self.cur.execute(c,values)
            if show:
                self.display("Result: Success",self.color)
        except BaseException as e:
            if show:
                self.display(f"Result: Failed \tError:{e}",self.eColor)
        
    def update(self,fieldNValues,conditions,show=True):
        fnv=""
        values = []
        print(fieldNValues)
        for field,value in fieldNValues:
            fnv += field + "= (?),"
            values.append(value)
        fnv=fnv[:-1]
        
        q = ""
        for field,op,value in conditions:
            values.append(value)
            q += f"{field} {op} (?) "
        
        c = f"UPDATE {self.name} SET {fnv} WHERE {q}"
        
        if show:
            self.display(f"Update Table:{self.name} \nCommand:{c}\tValues:{values}",self.color)
            
        try:
            self.cur.execute(c,values)
            if show:
                self.display("Result: Success",self.color)
        except BaseException as e:
            if show:
                self.display(f"Result: Failed \tError:{e}",self.eColor)
    
    def query(self,fieldNValues=None,fields=None,orderby='',show=False):
        result= []
        f = ""
        if (fields):
            for field in fields:
                f += field + ","
            f = f[:-1]
        else:
            f = "*"
            
        q = ""
        values = []
        if (fieldNValues):
            for field,op,value in fieldNValues:
                if type(value) == list:
                    values = value
                    v = ','.join("?" for vs in values)
                else:
                    values.append(value)
                    v = '?'
                q += f"WHERE {field} {op} ({v}) "
        
        if orderby:
            orderby = f'ORDER BY {orderby}'        
        
        c = f"SELECT {f} FROM {self.name} {q} {orderby}"
        
        if show:
            self.display(f"Query in Table:{self.name} \nCommand:{c}\tValues:{values}",self.color)
            
        try:
            self.cur.execute(c,values)
            result = self.cur.fetchall()
            if show:
                self.display(f"Result: Success:{result}",self.color)
        except BaseException as e:
            if show:
                self.display(f"Result: Failed \tError:{e}",self.eColor)
        
        return result
    
    def remove(self,value,field="ID",Operator="=",show=True):
        if self.fND[field].find("INTEGER") !=-1:
            value =  int(value)
        c = f"DELETE FROM {self.name} WHERE {field} {Operator} (?)"
        
        if show:
            self.display(f"Remove from Table:{self.name} \nCommand:{c}\tValue:{value}",self.color)
        
        try:
            self.cur.execute(c,[value])
            if show:
                self.display("Result: Success",self.color)
        except BaseException as e:
            if show:
                self.display(f"Result: Failed \tError:{e}",self.eColor)
    
    def destructure(self,FNT):
        extra = ''
        fND = {}
        if 'extra' in FNT:
            extra = FNT['extra']
        if 'FNDts' in FNT:
            fND = FNT['FNDts'].copy()
        return fND,extra