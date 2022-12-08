class Table:
    def __init__(self,conn,name,fieldNTypes,extra=None):
        self.conn = conn
        self.cur = conn.cursor()
        self.name = name
        self.fND = {}
        
        self.create(fieldNTypes,extra)
    
    def createTxt(self,fieldNTypes,extra):
        create = f"CREATE TABLE {self.name} ("
        
        for field,type in fieldNTypes.items():
            self.fND[field]=type
            create += f"{field} {type},"
        if extra:
            create += extra
        else:
            create = create[:-1]
        create += ")"
        
        return create
    
    def create(self,fieldNTypes,extra):
        c = self.createTxt(fieldNTypes,extra)
        try:
            self.conn.execute(c)
        except Exception as e:
            print(f"DBError:{e}")

    def insert(self,fieldNValues):
        fields = "("
        sValues = "("
        values = []
        for field,value in fieldNValues.items():
            fields += field + ","
            sValues += "?,"
            values.append(value)
        fields = fields[:-1] + ")"
        sValues = sValues[:-1] + ")"
        
        i = f"INSERT INTO {self.name} {fields} VALUES {sValues}"
        print(f"--------\nTable:{self.name} \n Operation:Insert \n command:{i} \n values:{values} \n--------")
        self.cur.execute(i,values)
        self.conn.commit()
    
    def query(self,fieldNValues=None,fields=None,order=""):
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
                values.append(value)
                q += f"WHERE {field} {op} (?) "
                
        d = f"SELECT {f} FROM {self.name} {q} {order}"
        
        self.cur.execute(d,values)
        result = self.cur.fetchall()
        print(f"--------\nTable:{self.name} \n Operation:Query \n command:{d} \n values:{values} \n Result:{result}\n--------")
        return result
    
    def remove(self,value,field="ID",Operator="="):
        if self.fND[field].find("INTEGER") !=-1:
            value =  int(value)
        d = f"DELETE FROM {self.name} WHERE {field} {Operator} (?)"
        
        print(f"--------\nTable:{self.name} \n Operation:Remove \n command:{d} \n values:{value} \n--------")
        self.cur.execute(d,[value])
        self.conn.commit()
        return
            