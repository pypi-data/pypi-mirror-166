##version==0.0.6##
class alphabet:
    def __init__(self,sym) -> None:
      self.sym=sym

    def A(self,n, s="A"):
        if self.sym!=None:
          s=self.sym
        if n==0:
            print(" "*3+s+" "*3,end="  ")
        elif n==1:
            print(" "*2+s+" "+s+" "*2,end="  ")
        elif n==2:
            print(" "+s*5+" ",end="  ")
        elif n==3:
            print(" "+s+" "*3+s+" ",end="  ")
        elif n==4:
            print(" "+s+" "*3+s+" ",end="  ")

    def B(self,n,s="B"):
        if self.sym!=None:
          s=self.sym      
        if n==0 or n==2 or n==4:
            print(s*4+" ",end="  ")
        else:
            print(s+" "*3+s,end="  ")

    def C(self,n,s="C"):
        if self.sym!=None:
          s=self.sym      
        if n==0 or n==4:
          print(" "+s*4,end="  ")
        else:
          print(s+" "*4,end="  ")

    def D(self,n,s="D"):
      if self.sym!=None:
        s=self.sym       
      if n==0 or n==4:
        print(s*4+" ",end="  ")
      else:
        print(" "+s+" "*2+s,end="  ") 

    def E(self,n,s="E"):
      if self.sym!=None:
        s=self.sym     
      if n==1 or n==3:
        print(s+" "*4,end="  ")
      else:
        print(s*5,end="  ") 

    def F(self,n,s="F"):
      if self.sym!=None:
        s=self.sym       
      if n==1 or n==3 or n==4:
        print(s+" "*4,end="  ")
      else:
        print(s*5,end="  ")

    def G(self,n,s="G"):
      if self.sym!=None:
        s=self.sym       
      if n==0 or n==4:
        print(' '+s*4,end="  ")
      elif n==1:
        print(s+' '*4,end="  ")
      elif n==2:
        print(s+' '+s*3,end='  ')
      elif n==3:
        print(s+' '+s+' '+s,end="  ")  

    def H(self,n,s="H"):
      if self.sym!=None:
        s=self.sym        
      if (n==0 or n==1 or n==3 or n==4):
        print(s+" "*3+s,end="  ")
      elif n==2:
        print(s*5,end="  ")
    
    def I(self,n,s="I"):
      if self.sym!=None:
        s=self.sym        
      if(n==0 or n==4):
        print(s*5,end="  ")
      else:
        print(" "*2+s+" "*2,end="  ")

    def J(self,n,s="J"):
      if self.sym!=None:
        s=self.sym        
      if n==0:
        print(s*5,end="  ")
      elif n==1 or n==2:
        print(" "*2+s+" "*2,end="  ")    
      elif n==3 or n==4:
        print(s+" "+s+" "*2,end="  ")  

    def K(self,n,s="K"):
      if self.sym!=None:
        s=self.sym        
      if n==0 or n==4:
        print(s+' '*2+s,end="  ")
      elif n==1 or n==3:
        print(s+' '+s+' ',end="  ")
      elif n==2:
        print(s*2+' '*2,end="  ") 

    def L(self,n,s="L"):
      if self.sym!=None:
        s=self.sym        
      if(n==0 or n==1 or n==2 or n==3):
        print(s+4*" ",end="  ")
      elif(n==4):
        print(s*5,end="  ")

    def M(self,n,s="M"):
      if self.sym!=None:
        s=self.sym        
      if n==0 or n==3 or n==4:
        print(s+" "*3+s,end="  ")
      elif n==1:
        print(s*2+" "+s*2,end="  ")
      elif n==2:
        print(s+" "+s+" "+s,end="  ")

    def O(self,n,s="O"):
      if self.sym!=None:
        s=self.sym        
      if n==0 or n==4:
        print(" "+s*3+" ",end="  ")
      else:
        print(s+" "*3+s,end="  ")

    def N(self,n,s="N"):
      if self.sym!=None:
        s=self.sym        
      if n==0 or n==4:
        print(s+" "*3+s,end="  ")
      elif n==1:
        print(s*2+" "*2+s,end="  ")
      elif n==2:
        print(s+" "+s+" "+s,end="  ")
      elif n==3:
        print(s+" "*2+s*2,end="  ")

    def P(self,n,s="P"):
      if self.sym!=None:
        s=self.sym        
      if n==0 or n==2:
        print(s*5,end="  ")
      elif n==1:
        print(s+' '*3+s,end="  ")
      elif n==3 or n==4:
        print(s+' '*4,end="  ")

    def Q(self,n,s="Q"):
      if self.sym!=None:
        s=self.sym        
      if n==4:
        print(' '*4+s+' '*2,end="  ")
      elif n==0:
        print(' '+s+' '+s+' '*3,end="  ")
      elif n==1:
        print(s*2+' '*2+s+' '*2,end="  ")
      elif n==2:
        print(s+' '+s+' '+s+' '*2,end="  ")
      elif n==3:
        print(' '+s+' '+s+' '*3,end="  ")

    def S(self,n,s="S"):
      if self.sym!=None:
        s=self.sym        
      if n==0 or n==2 or n==4:
        print(s+' '+s+' '+s,end="  ")
      elif n==1:
        print(s+" "*4,end="  ")
      elif n==3:
        print(" "*4+s,end="  ")

    def R(self,n,s="R"):
      if self.sym!=None:
        s=self.sym        
      if n==0:
        print(s*5,end="  ")
      elif n==1:
        print(s+" "*3+s,end="  ")
      elif n==2:
        print(s*5,end="  ")
      elif n==3:
        print(s+" "+s+" "*2,end="  ")
      elif n==4:
        print(s+" "*2+s*2,end="  ")

    def T(self,n,s="T"):
      if self.sym!=None:
        s=self.sym        
      if n==0:
        print(s*5,end="  ")
      else:
        print(" "*2+s+" "*2,end="  ")

    def U(self,n,s="U"):
      if self.sym!=None:
        s=self.sym        
      if n==4:
        print(" "+s*3+" ",end="  ")
      else:
        print(s+" "*3+s,end="  ")

    def V(self,n,s="V"):
      if self.sym!=None:
        s=self.sym        
      if n==0 or n==1 or n==2:
        print(s+" "*3+s,end="  ")
      elif n==3:
        print(" "+s+" "+s+" ",end="  ")
      elif n==4:
        print(" "*2+s+" "*2,end="  ")

    def W(self,n,s="W"):
      if self.sym!=None:
        s=self.sym        
      if n==0 or n==1:
        print(s+' '*5+s,end='  ')
      elif n==2:
        print(s+' '*2+s+' '*2+s,end="  ")
      elif n==3:
        print(s+' '+s+' '+s+' '+s,end='  ')
      elif n==4:
        print(' '+s+' '*3+s+' ',end="  ")

    def X(self,n,s="X"):
      if self.sym!=None:
        s=self.sym        
      if n==0 or n==4:
        print(s+' '*3+s,end="  ")
      elif n==1 or n==3:
        print(' '+s+' '+s+' ',end="  ")
      elif n==2:
        print(' '*2+s+' '*2,end="  ")    

    def Y(self,n,s="Y"):
      if self.sym!=None:
        s=self.sym        
      if n==3 or n==4 or n==2:
        print(' '*2+s+' '*2,end="  ")
      elif n==0:
        print(s+' '*3+s,end="  ")
      elif n==1:
        print(' '+s+' '+s+' ',end="  ")

    def Z(self,n,s="Z"):
      if self.sym!=None:
        s=self.sym        
      if n==0 or n==4:
        print(s*5,end="  ")
      elif n==2:
        print(' '*2+s+' '*2,end="  ")
      elif n==1:
        print(' '*3+s+' ',end="  ")
      elif n==3:
        print(' '+s+' '*3,end="  ")

    def space():
      print(" "*5,end="  ")

    def fullstop(self,n,s="*"):
      if self.sym!=None:
        s=self.sym        
      if n==4:
        print(' '+s+' ',end="  ")
      else:
        print(" "*3,end="  ")

class number:
    def __init__(self,sym) -> None:
      self.sym=sym

    def zero_0(self,n,s="0"):
      if self.sym!=None:
        s=self.sym
      elif n==0 or n==4:
        print(" "+s*2+" ",end="  ")    
      else:
        print(s+" "*2+s,end="  ")

    def one_1(self,n,s="1"):
      if self.sym!=None:
        s=self.sym        
      if n==0 or n==3:
        print(" "*2+s+" "*2,end="  ")
      elif n==1:
        print(" "+s*2+" "*2,end="  ")
      elif n==2:
        print(s+" "+s+" "*2,end="  ")
      elif n==4:
        print(s*5,end="  ")    

    def two_2(self,n,s="2"):
      if self.sym!=None:
        s=self.sym 
      if n==4:
        print(s*4,end="  ")    
      elif n==0:
        print(" "+s*2+" ",end="  ")
      elif n==1:
        print(s+" "*2+s,end="  ")
      elif n==2:
        print(" "*2+s+" ",end="  ")
      elif n==3:  
        print(" "+s+" "*2,end="  ")

    def three_3(self,n,s="3"):
      if self.sym!=None:
        s=self.sym     
      if n==0 or n==4:
        print(" "+s*2+" ",end="  ")
      elif n==1 or n==3:
        print(s+" "*2+s,end="  ")
      elif n==2:
        print(" "*2+s+" ",end="  ")

    def four_4(self,n,s="4"):
      if self.sym!=None:
        s=self.sym     
      if n==0:
        print(" "*3+s+" ",end="  ")
      elif n==1:
        print(" "*2+s*2+" ",end="  ")
      elif n==3:
        print(s*5,end="  ")
      elif n==4:
        print(" "*3+s+" ",end="  ")  
      elif n==2:
        print(" "+s+" "+s+" ",end="  ")

    def five_5(self,n,s="5"):
      if self.sym!=None:
        s=self.sym          
      if n==0:
        print(s*5,end="  ")
      elif n==1:
        print(s+" "*4,end="  ")
      elif n==2 or n==4:
        print(s*4+" ",end="  ")
      elif n==3:
        print(" "*4+s,end="  ")

    def six_6(self,n,s="6"):
      if self.sym!=None:
        s=self.sym 
      if n==0 or n==2 or n==4:
        print(s*4,end="  ")
      elif n==1:
        print(s+" "*3,end="  ")
      elif n==3:
        print(s+" "*2+s,end="  ")      

    def seven_7(self,n,s="7"):
      if self.sym!=None:
        s=self.sym 
      if n==0 :
        print(s*5,end="  ")
      elif n==2:
        print(' '*2+s+' '*2,end="  ")
      elif n==1:
        print(' '*3+s+' ',end="  ")
      elif n==3:
        print(' '+s+' '*3,end="  ")
      elif n==4:
        print(s+' '*4,end="  ")  

    def eight_8(self,n,s="8"):
      if self.sym!=None:
        s=self.sym 
      if n==0 or n==2 or n==4:
        print(s*4,end="  ")        
      elif n==3 or n==1:
        print(s+" "*2+s,end="  ")

    def nine_9(self,n,s="9"):
      if self.sym!=None:
        s=self.sym 
      if n==0 or n==2 or n==4:
        print(s*4,end="  ")          
      elif n==1:
        print(s+" "*2+s,end="  ")
      elif n==3:
        print(" "*3+s,end="  ")  

def help():
  print()
  print("*********************************************************")
  print("This program has been written by Harsh Gupta.")
  print("This program can be used to display the given input into figlet fonts :)\n")
  print("Syntax >>>myfiglet.display(<input string>,<symbol>)\n")
  print("For example.......")
  print(">>>myfiglet.display('Python','%')\n")
  print("OUTPUT:")
  display("Python",'%')
  print("For example.......")
  print("TO PRINT FIGLET WITH SELF BUILDING CHARACTERS USE: pattern='name'\n")
  print("For example.......")
  print(">>>myfiglet.display('Python',pattern='name')")
  print("OUTPUT:")
  display("Python",pattern="name")
  print("Second argument '<symbol>' in dispaly() is optional and is by default '*'\n")
  print("IF YOU WANT TO ADD COLOURS TO YOUR FIGLET FONT : use <color> parameter ")
  print("For example.......")
  print(">>>myfiglet.display('Python','@',colour='red')")
  print("OUTPUT:")
  display("Python","@",colour='red')
  print("TO DISPLAY BRIGHT COLOURS TYPE:")
  print("   >>>myfiglet.display('Python','@',colour='yellow',bright=True)\n")
  print("TO VIEW ALL AVAILABLE COLOUR SCHEMES TYPE:")
  print("   >>>myfiglet.colour_help()\n")
  print("TO ADD RAINBOW COLOUR EFFECT TO YOUR FIGLET TYPE:")
  print("   >>>myfiglet.display('Python','@',rainbow=True)")
  print("OUTPUT:")
  display("Python","@",rainbow=True)
  print("*********************************************************")

def colour_help():
  print("|----------------------------------------------|")
  print("|     colour=    |    CORRESPONDING COLOUR     |")
  print("|----------------------------------------------|")
  print("|     'black'    |        Dark Black           |")
  print("|     'red'      |        Dark Red             |")
  print("|     'green'    |        Dark Green           |")
  print("|     'yellow'   |        Yellow               |")
  print("|     'blue'     |        Blue                 |")
  print("|     'magenta'  |        Dark Magenta         |")
  print("|     'cyan'     |        Cyan                 |")
  print("|     'white'    |        Pure White           |")
  print("|----------------------------------------------|")

class control:
  def main(obj_alph,obj_num,name):
    for i in range(0,5):
      if rainbow_schema==1:
        print(rainbow_colour[i],end="")
      for k in range(0,len(name)):
        if name[k]==' ':
          alphabet.space()
        elif name[k]=='.':
          alphabet.fullstop(obj_alph,i)
        elif name[k]=="a" or name[k]=="A":
          alphabet.A(obj_alph,i)         
        elif name[k]=="b" or name[k]=="B":
          alphabet.B(obj_alph,i)
        elif name[k]=="c" or name[k]=="C":
          alphabet.C(obj_alph,i)
        elif name[k]=="d" or name[k]=="D":
          alphabet.D(obj_alph,i)
        elif name[k]=="e" or name[k]=="E":
          alphabet.E(obj_alph,i)     
        elif name[k]=="f" or name[k]=="F":
          alphabet.F(obj_alph,i) 
        elif name[k]=="g" or name[k]=="G":
          alphabet.G(obj_alph,i)                    
        elif name[k]=="h" or name[k]=="H":
          alphabet.H(obj_alph,i)
        elif name[k]=="i" or name[k]=="I":
          alphabet.I(obj_alph,i)
        elif name[k]=="j" or name[k]=="J":
          alphabet.J(obj_alph,i)    
        elif name[k]=="k" or name[k]=="K":
          alphabet.K(obj_alph,i)                     
        if name[k]=="l" or name[k]=="L":
          alphabet.L(obj_alph,i)
        elif name[k]=="m" or name[k]=="M":
          alphabet.M(obj_alph,i)      
        elif name[k]=="n" or name[k]=="N":
          alphabet.N(obj_alph,i)
        elif name[k]=="o" or name[k]=="O":
          alphabet.O(obj_alph,i)
        elif name[k]=="p" or name[k]=="P":
          alphabet.P(obj_alph,i) 
        elif name[k]=="q" or name[k]=="Q":
          alphabet.Q(obj_alph,i)              
        elif name[k]=="r" or name[k]=="R":
          alphabet.R(obj_alph,i)
        elif name[k]=="s" or name[k]=="S":
          alphabet.S(obj_alph,i)
        elif name[k]=="t" or name[k]=="T":
          alphabet.T(obj_alph,i)     
        elif name[k]=="u" or name[k]=="U":
          alphabet.U(obj_alph,i)
        elif name[k]=="v" or name[k]=="V":
          alphabet.V(obj_alph,i)
        elif name[k]=="w" or name[k]=="W":
          alphabet.W(obj_alph,i)
        elif name[k]=="x" or name[k]=="X":
          alphabet.X(obj_alph,i) 
        elif name[k]=="y" or name[k]=="Y":
          alphabet.Y(obj_alph,i) 
        elif name[k]=="z" or name[k]=="Z":
          alphabet.Z(obj_alph,i)        
        elif name[k]=="0":
          number.zero_0(obj_num,i)                  
        elif name[k]=="1":
          number.one_1(obj_num,i)           
        elif name[k]=="2":
          number.two_2(obj_num,i) 
        elif name[k]=="3":
          number.three_3(obj_num,i)      
        elif name[k]=="4":
          number.four_4(obj_num,i) 
        elif name[k]=="5":
          number.five_5(obj_num,i)     
        elif name[k]=="6":
          number.six_6(obj_num,i)          
        elif name[k]=="7":
          number.seven_7(obj_num,i) 
        elif name[k]=="8":
          number.eight_8(obj_num,i)
        elif name[k]=="9":
          number.nine_9(obj_num,i)                                                                                
      print()
      

reset='\u001b[0m'
rainbow_colour={0:'\u001b[35m',1:'\u001b[34m',2:'\u001b[32m',3:'\u001b[33m',4:'\u001b[31m'}
colour_scheme={'bright black':'\u001b[30;1m','bright red':'\u001b[31;1m','bright green':'\u001b[32;1m','bright yellow':'\u001b[33;1m','bright blue':'\u001b[34;1m','bright magenta':'\u001b[35;1m','bright cyan':'\u001b[36;1m','bright white':'\u001b[37;1m','black':'\u001b[30m','red':'\u001b[31m','green':'\u001b[32m','yellow':'\u001b[33m','blue':'\u001b[34m','magenta':'\u001b[35m','cyan':'\u001b[36m','white':'\u001b[37m'}
def colour_check(colour,bright):
  try:
    if bright==True:
      return colour_scheme['bright '+colour]
    else:  
      return colour_scheme[colour]
  except:
    return "You choose Invalid colour !!!\n"

rainbow_schema=0
def display(name,symbol='*',rainbow=False,pattern=None,colour=None,bright=False):
  if rainbow==True:
    global rainbow_schema
    rainbow_schema=1
  elif colour !=None:
    print(colour_check(colour,bright))
  if pattern=="name":
    alph=alphabet(None)
    num=alphabet(None)
    control.main(alph,num,name)
    print(reset)
  else:
    alph=alphabet(symbol)
    num=alphabet(symbol)
    control.main(alph,num,name)
    print(reset)

