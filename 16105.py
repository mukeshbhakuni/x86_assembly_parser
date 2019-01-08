#[i for i in range(len(d)) for j in d if j=="a" ][-1] taking element from dictionary
# name=type,value,size,d/u

import sys
import json

# this generates  symbol table for the given assembly code.  
class symbolTable:
    def __init__(self):
        self.address=0
        self.symbol={}
        self.types=["dd","db","dw","dq"]
        self.res_types=["resd","resb","resw","resq"]
        self.extern=["global","extern"]
        self.branch=["jmp","loop"]
        self.reg=["eax","ax","al","ah","ecx","cx","cl","ch","edx","dx","dl","dh","ebx","bx","bl","bh","esp","sp","ebp","bp","esi","si","edi","di"]
        self.ins=["mov","add","sub"]
    def get_size(self,val,_type):             #gets the size of type of variable used    
        if _type=="dd" or _type=="resd":
            val=val.split(',')
            val=map(int,val)
            return len(val)*4
        elif _type=="db":
            return len(val)
        elif _type=="resb":
            return int(val)
        elif _type=="dq" or _type=="resq":
            val=val.split(',')
            val=map(float,val)
            return len(val)*8
    def get_value(self,val,_type):           #gets the value of the variable used
        if _type=="dd":
            val=''.join(val)
            val=val.split(',')
            val=map(int,val)
            if len(val)>1:
                return val
            else:
                return val[0]
        elif _type=="dq":
            val=''.join(val)
            val=val.split(',')
            val=map(float,val)
            if len(val)>1:
                return val
            else:
                return val[0]   
        elif _type=="db":
            val=' '.join(val)
            if val[(len(val)-5):]==',10,0':
                val=filter(lambda x:x!="\"",val[:len(val)-5])
                return val
            elif val[(len(val)-2):]==',0':
                val=filter(lambda x:x!="\"",val[:len(val)-2])
                return val
            else:
                val=filter(lambda x:x!="\"",val)
                return val
            
            
    def add(self,a,x):
        self.symbol[a]=x
    def validate(self,x):               #validation
        if len(x)>2:
            if x[1] in self.types and x[0] not in self.symbol and self.address==0:
                size=self.get_size(' '.join(x[2:]),x[1])
                self.symbol[x[0]]=[x[1],"D",self.get_value(x[2:],x[1]),size,"00000000"]
                self.address+=size    
            elif x[1] in self.types and x[0] not in self.symbol and self.address!=0:
                _size=self.get_size(' '.join(x[2:]),x[1])
                self.symbol[x[0]]=[x[1],"D",self.get_value(x[2:],x[1]),_size,('0'*(8-len(hex(self.address)[2:])))+(''.join(map(self.caseChange,hex(self.address)[2:])))]
                self.address+=_size
            elif x[1] in self.res_types and x[0] not in self.symbol and self.address==0:
                _size=self.get_size(x[2],x[1])
                self.symbol[x[0]]=[x[1],"D",[],_size,'00000000']
                self.address+=_size
            elif x[1] in self.res_types and x[0] not in self.symbol and self.address!=0:
                _size=self.get_size(x[2],x[1])
                self.symbol[x[0]]=[x[1],"D",[],_size,('0'*(8-len(hex(self.address)[2:])))+(''.join(map(self.caseChange,hex(self.address)[2:])))]
                self.address+=_size
            elif x[0] in self.symbol:
                print "__symbol |<"+x[0]+">| declared more than once"
                sys.exit()    
        elif len(x)==2:     
            if x[0] in self.extern:
                if x[1] not in self.symbol:
                    self.symbol[x[1]]=[x[0],"D",[],"",""]
                else:
                    print "__symbol |<"+x[1]+">| declared more than once"
                    sys.exit()
                
    def caseChange(self,x):
        if x in "abcdef":
            return chr(ord(x)-32)
        return x            
    def display(self):
        print self.symbol


# this generates the literal table for the assembly code
class literal_table:
    def __init__(self):
        self.literal={}
    def display(self):
        print self.literal
class eflags:
    def __init__(self):
        self.flags={}
        self.flags["cf"]=0
        self.flags["zf"]=0
        self.flags["nf"]=0
        self.flags["df"]=0
    def display(self):
        print self.flags



# this generates the opcode table for the assembly code.
class opcode_table:
    def __init__(self):
        self.address=0
        self.ins_code=[]
        self.opr_opcode=[]
        self.mem_addr=[]   
        self.values=[]
        self.reg32=["eax","ecx","edx","ebx","esp","ebp","esi","edi"]        
        self.binary=["000","001","010","011","100","101","110","111"]
        with open("a.json") as fp:
            self.insCode=json.load(fp)
    def addReg(self,opcode,reg):
        return map(lambda x:self.changeCase(x),hex(int(opcode,16)+reg)[2:])
    def changeCase(self,x):
        if x in "abcdef":
            return chr(ord(x)-32)
        return x    

    def changeHexAdd(self,x):
        x=''.join(map(self.changeCase,(hex(int(x))[2:]))) 
        return ('0'*(8-len(x))+x)
    def genInsCode(self,line,ins,st):
        n=""
        m=""
        p=""
        if ins=="mov":
            if line[0][:5]=="dword":
                a=sep_var(line[0])
                if a in self.reg32 and line[1] in self.reg32:
                    self.opr_opcode+=[self.insCode[ins][2]]
                    self.mem_addr+=[""]
                    self.values+=[""]
                    m="00"
                    n=self.binary[(self.reg32.index(line[1]))]
                    p=self.binary[(self.reg32.index(a))]
                elif a in self.reg32 and line[1] not in self.reg32 and line[1] not in st.symbol:
                    self.opr_opcode+=[self.insCode[ins][3]]
                    self.values+=[self.changeHexAdd(line[1])]
                    self.mem_addr+=[""]
                    m="00"
                    n=self.binary[(self.reg32.index(a))]
                    p=""                    
                elif a not in self.reg32 and line[1] in self.reg32:
                    self.opr_opcode+=[self.insCode[ins][2]]
                    m="00"
                    self.mem_addr+=[st.symbol[a][4]]
                    self.values+=[""]
                    n=self.binary[(self.reg32.index(line[1]))]
                    p="101"
                elif a not in self.reg32 and line[1] not in self.reg32:
                    self.opr_opcode+=[self.insCode[ins][3]]
                    self.mem_addr+=[st.symbol[a][4]]
                    self.values+=[self.changeHexAdd(line[1])]
                    m="00"
                    n="101"
                    p=""
            else:
                if line[0] in self.reg32 and line[1] in self.reg32:
                    m='11'
                    n=self.binary[self.reg32.index(line[1])]
                    p=self.binary[self.reg32.index(line[0])]
                    self.opr_opcode+=[self.insCode[ins][2]]
                    self.mem_addr+=[""]
                    self.values+=[""]
                elif line[0] in self.reg32 and line[1] not in self.reg32 and line[1][:6]!="dword[":
                    if line[1] not in st.symbol:
                        self.opr_opcode+=[map(self.changeCase,(hex(184+self.reg32.index(line[0]))[2:]))]
                        #print self.changeHexAdd(line[1])
                        self.mem_addr+=[""]
                        self.values+=[self.changeHexAdd(line[1])]
                    else:
                        self.opr_opcode+=[""]
                        m="10"
                        n="111"
                        p=self.binary[self.reg32.index(line[0])]
                        self.values+=[""]
                        self.mem_addr+=[st.symbol[line[1]][4]]   
                elif line[1][:6]=="dword[":
                    a=sep_var(line[1])
                    if a in self.reg32:
                        self.opr_opcode+=[self.insCode[ins][1]]
                        m="00"
                        self.mem_addr+=[""]
                        self.values+=[""]  
                        p=self.binary[(self.reg32.index(a))]
                        n=self.binary[(self.reg32.index(line[0]))]
                    elif a not in self.reg32:
                        self.opr_opcode+=[self.insCode[ins][1]]
                        m="00"
                        self.mem_addr+=[st.symbol[a][4]]
                        self.values+=[""]
                        n=self.binary[self.reg32.index(line[0])]
                        p="101"
            return (m+n+p)             
        elif ins=="add":
            if line[0][:5]=="dword":
                a=sep_var(line[0])
                if a in self.reg32:
                    m="00"
                    if line[1] in self.reg32:
                        n=self.binary[self.reg32.index(line[1])]
                        p=self.binary[self.reg32.index(a)]
                        self.opr_opcode+=[self.insCode[ins][0]]
                        self.mem_addr+=[""]
                        self.values+=[""]
                    else:
                        n="000"
                        p=self.binary[self.reg32.index(a)]        
                        self.opr_opcode+=[self.insCode[ins][2]]
                        self.mem_addr+=[""]
                        self.values+=[self.changeHexAdd(line[1])]
                else:
                    m="00"
                    if line[1] in self.reg32:
                        n=self.binary[self.reg32.index(line[1])]
                        p="101"
                        self.mem_addr+=[st.symbol[a][4]]
                        self.values+=[""]
                        self.opr_opcode+=[self.insCode[ins][0]]
                    else:
                        self.mem_addr+=[st.symbol[a][4]]
                        self.values+=[self.changeHexAdd(line[1])]
                        n="000"
                        p="101"
                        self.opr_opcode+=[self.insCode[ins][2]]
            else:
                if line[1][:5]=="dword":
                    a=sep_var(line[1])
                    m="00"
                    if a in self.reg32:
                        self.opr_opcode+=[self.insCode[ins][1]]
                        n=self.binary[self.reg32.index(line[0])]
                        p=self.binary[self.reg32.index(a)]
                        self.mem_addr+=[""]
                        self.values+=[""]
                    else:
                        self.opr_opcode+=[self.insCode[ins][1]]
                        p='101'
                        n=self.binary[self.reg32.index(line[0])]
                        self.values+=[""]
                        self.mem_addr+=[st.symbol[a][4]]
                elif line[1] in self.reg32:
                    m="11"
                    self.opr_opcode+=[self.insCode[ins][0]]
                    n=self.binary[self.reg32.index(line[1])]
                    p=self.binary[self.reg32.index(line[0])]
                    self.mem_addr+=[""]
                    self.values+=[""]
                else:
                    m="11"
                    self.opr_opcode+=[self.insCode[ins][2]]
                    self.values+=[self.changeHexAdd(line[1])]
                    self.mem_addr+=[""]
            return (m+n+p)        
        elif ins=="sub":
            if line[0][:5]=="dword":
                a=sep_var(line[0])
                if a in self.reg32:
                    m="00"
                    if line[1] in self.reg32:
                        n=self.binary[self.reg32.index(line[1])]
                        p=self.binary[self.reg32.index(a)]
                        self.opr_opcode+=[self.insCode[ins][0]]
                        self.mem_addr+=[""]
                        self.values+=[""]
                    else:
                        n="101"
                        p=self.binary[self.reg32.index(a)]        
                        self.opr_opcode+=[self.insCode[ins][2]]
                        self.mem_addr+=[""]
                        self.values+=[self.changeHexAdd(line[1])]
                else:
                    m="00"
                    if line[1] in self.reg32:
                        n=self.binary[self.reg32.index(line[1])]
                        p="101"
                        self.opr_opcode+=[self.insCode[ins][0]]
                        self.mem_addr+=[st.symbol[a][4]]
                        self.values+=[""]
                    else:
                        n="101"
                        p="101"
                        self.opr_opcode+=[self.insCode[ins][2]]
                        self.mem_addr+=[st.symbol[a][4]]
                        self.values+=[self.changeHexAdd(line[1])]
            else:
                if line[1][:5]=="dword":
                    a=sep_var(line[1])
                    m="00"
                    if a in self.reg32:
                        self.opr_opcode+=[self.insCode[ins][1]]
                        n=self.binary[self.reg32.index(line[0])]
                        p=self.binary[self.reg32.index(a)]
                        self.mem_addr+=[""]
                        self.values+=[""]
                    else:
                        self.opr_opcode+=[self.insCode[ins][1]]
                        p='101'
                        n=self.binary[self.reg32.index(line[0])]
                        self.values+=[""]
                        self.mem_addr+=[st.symbol[a][4]]
                elif line[1] in self.reg32:
                    m="11"
                    self.opr_opcode+=[self.insCode[ins][0]]
                    n=self.binary[self.reg32.index(line[1])]
                    p=self.binary[self.reg32.index(line[0])]
                    self.mem_addr+=[""]
                    self.values+=[""]
                else:
                    m="11"
                    self.opr_opcode+=[self.insCode[ins][2]]
                    n="101"
                    p=self.binary[self.reg32.index(line[0])]
                    self.values+=[self.changeHexAdd(line[1])]
                    self.mem_addr+=[""]
            return (m+n+p)
        elif ins=="lodsb":
            self.mem_addr+=[""]
            self.values+=[""]
            self.opr_opcode+=[self.insCode[ins][0]]
            return (m+n+p)
        elif ins=="stosb":
            self.mem_addr+=[""]
            self.values+=[""]
            self.opr_opcode+=[self.insCode[ins][0]]
            return (m+n+p)
        elif ins=="cld":
            self.mem_addr+=[""]
            self.values+=[""]
            self.opr_opcode+=[self.insCode[ins][0]]
            return (m+n+p)
        elif ins=="std":
            self.mem_addr+=[""]
            self.values+=[""]
            self.opr_opcode+=[self.insCode[ins][0]]
            return (m+n+p)
        elif ins=="movsb":
            self.mem_addr+=[""]
            self.values+=[""]
            self.opr_opcode+=[self.insCode[ins][0]]      
            return (m+n+p)
        elif ins=="rep":
            if line[0]=='scasb':
                self.mem_addr+=[""]
                self.values+=[""]
                self.opr_opcode+=[(self.insCode[ins][0])+self.insCode['scasb'][0]]
            else:
                self.mem_addr+=[""]
                self.values+=[""]
                self.opr_opcode+=[self.insCode[ins][0]]
            return (m+n+p)                    












                        



            
            
            
                        
                    
                    
                    
                    
                    
                    

    def convertToHex(self,x):
        for i in range(len(x)):
            if x[i]!='' and x[i]!=None:
                x[i]=hex(int(x[i],2))[2:]
        return x         
    def display(self):
        x=zip(map(lambda x:''.join(x),self.opr_opcode),self.convertToHex(self.ins_code),self.mem_addr,self.values)
        for i in x:
            y=(i[0],''.join(map(self.changeCase,i[1])),str([i[2]]),i[3])
            addr=self.changeHexAdd(str(self.address))
            addr='0'*(8-len(addr))+addr
            tot=''.join(filter(lambda s:s!='[\'\']',y))
            print ' '.join([addr,tot])
            self.address+=(sum(map(len,y))/2)
             
    def codeGen(self,line,st):
        n=len(line)
        if(n>=3):
            if(n>3):
                line=line[1:]
            self.ins_code+=[self.genInsCode(line[1:],line[0],st)]
        elif(n==1):
            self.ins_code+=[self.genInsCode(line[1:],line[0],st)]
        elif(n==2):
            self.ins_code+=[self.genInsCode(line[1:],line[0],st)]

            
            
            
                
        
        
        
def add_literal(lt,val):
    if val[0]=='"':
        if val[0]=='"' and val[-1]=='"':
            lt.literal[val[1:len(val)-1]]=["char",len(val)-2]
    elif is_num(val):
            lt.literal[val]=['int',4]
    else:
        print "invalid literal <"+val+">"
        sys.exit()
        
    
def sep_var(x):
    x=''.join((''.join(x.split('dword[')).split(']')))
    x=''.join((''.join(x.split('byte[')).split(']')))
    return x

def concat_list(x):
    return [i for j in x for i in j]
    
def seperate(line):
    n=len(line)
    if n==1:
        line[0]=line[0].split(":")
        line=concat_list(line)
        line=filter(lambda x:x!='',line)
        return line
    elif n==2:  
        if ":" in line[0]:
            line[0]=line[0].split(":")
            line[1]=line[1].split(",")
            line=concat_list(line)
            line=filter(lambda x:x!='',line)
            return line
        else:
            line[0]=line[0].split(' ')
            line[1]=line[1].split(',')
            line=concat_list(line)
            line=filter(lambda x:x!='',line)
            return line
    elif n==3:
        line[0]=line[0].split(":")
        line[2]=line[2].split(",")
        line[1]=line[1].split(" ")
        line=concat_list(line)
        line=filter(lambda x:x!='',line)
        return line

def is_alpha(x):
    a="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if x[0] in a:
        return 1
    else:
        return 0



def is_num(x):
    a="0123456789"
    A=filter(lambda y:y in a,x)
    if x==A:
        return 1
    return 0
    
def validate_instructions(lines,st,lt,i):
    flag1=0
    flag2=0
    line=lines[i]
    n=len(line)
    if n==1:
        if line[0]!="ret" or line[0]!="main":
            if line[0] not in st.symbol:
                st.symbol[line[0]]=["func","D","",-1]
            else:
                print "__>loop |<"+line[0]+">| already exists"
                sys.exit()
    elif n==2:
        if line[0] in st.branch:
            if line[1] not in st.symbol and line[1]!="ret":
                st.symbol[line[1]]=["func","U","",-1]
                
    elif n==3: 
        if line[1][:6]=="dword[" and line[2][:6]=="dword[":
            print "__> memory to memory transfer not possible or something invalid"
            sys.exit()
        elif line[1][:6]=="dword[":
            flag1=1
        elif line[2][:6]=="dword[":
            flag2=1
        line=map(sep_var, line)
        if line[0] in st.ins:
            if line[1] not in st.reg and line[2] not in st.reg and flag1!=1:   ############here
                print "__> memory to memory transfer not possible or something invalid"
                sys.exit()
            elif line[1] in st.reg:
                if is_alpha(line[2]) and line[2] not in st.symbol and line[2] not in st.reg and flag2==1:
                    print "__>symbol <"+line[2]+">  used but not defined"
                    sys.exit()
                elif line[2] not in st.symbol and line[2] not in st.reg and flag2==0:
                    add_literal(lt,line[2])
            elif line[2] in st.reg:
                if is_alpha(line[1]) and line[1] not in st.symbol and line[1] not in st.reg and flag1==1:
                    print "__>symbol <"+line[1]+"> used but not defined"                    
                    sys.exit() ####################here
                elif line[1] not in st.symbol and line[1] not in st.reg and flag1==0 :
                    add_literal(lt,line[1])
            elif line[1][:6]=="dword[" and line[2] not in st.reg:
                add_literal(lt,line[2])

             
        else:
            print "invalid instruction <"+line[0]+">"
            sys.exit()
    elif n==4:
        if line[2][:6]=="dword[" and line[3][:6]=="dword[":
            print "__> memory to memory transfer not possible or something invalid"
            sys.exit()
        elif line[2][:6]=="dword[":
            flag1=0
        elif line[3][:6]=="dword[":
            flag2=0
        line=map(sep_var,line)
        if line[0] not in st.symbol:
            st.symbol[line[0]]=["func","D","",-1]
            if line[1] in st.ins:
                if line[2] not in st.reg and line[3] not in st.reg:
                    print "__> memory to memory transfer not possible or something invalid"
                    sys.exit()
                if line[2] in st.reg:
                    if is_alpha(line[3]) and line[3] not in st.symbol and  line[3] not in st.reg and flag1==1:
                        print "__>symbol <"+line[3]+">  used but not defined"
                        sys.exit()
                    elif line[3] not in st.symbol and  line[3] not in st.reg and flag1==0:
                        add_literal(lt,line[3])
                elif line[3] in st.reg:
                    if is_alpha(line[2]) and line[2] not in st.symbol and line[3] not in st.reg and flag2==1:
                        print "__>symbol <"+line[2]+">  used but not defined"
                        sys.exit()
                    elif line[2] not in st.symbol and line[3] not in st.reg and flag2==0:
                        add_literal(lt,line[2])   
            else:
                print "invalid instruction <"+line[0]+">"
                sys.exit()
        else:
            if st.symbol[line[0]][1]=="D":
                print"__> symbol as label <"+line[0]+"> redefined"
                sys.exit()
            elif st.symbol[line[0]][1]=="U":
                st.symbol[line[0]][1]='D'
            
     
#mov eax,ebx          

print "enter the asm file name : "
nm = raw_input()
fp=open(nm,"r+") 
text=fp.read()
lines=filter(lambda w:w!=[],map(lambda y:filter(lambda z:z!='',y),map(lambda x:x.split(' '),text.split("\n"))))
lines=map(lambda x:map(lambda y:filter(lambda z:z!='\t',y),x),lines)
st=symbolTable()
lt=literal_table()
ot=opcode_table()
ef=eflags()

k=None
for line in lines:
        if len(line)>1 and line[1]=='.data':
            st.address=0
        elif len(line)>1 and line[1]=='.bss':    
            st.address=0
        elif line[0].split(':')[0]!="main":
            st.validate(line)
        else:
            k=line
        
index=lines.index(k)
lines=lines[index:]


#change first one where main is starting (no insrtuction should be there after main: on the same line)

lines=map(seperate,lines)
print lines
ad=0
for i in range(1,len(lines)):
    validate_instructions(lines,st,lt,i)    
    ot.codeGen(lines[i],st)
    ef.display()
    
print "\nSYMBOL TABLE\n"
st.display()
print "\nLITERAL TABLE\n"
lt.display()
print "\nOPCODE TABLE\n"    
ot.display()
