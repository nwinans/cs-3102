# Code until next comment taken from https://nbviewer.jupyter.org/github/boazbk/tcscode/blob/master/Chap_07_TM.ipynb
import time, re, collections

def extractvars(src):
    varnames = re.findall( r'(?<!f)[a-zA-Z\_0-9]+', src, re.I | re.M)
    arrays = ["X","X_nonblank","Y","Y_nonblank"]
    scalars = []
    for t in varnames:
        if t in ['i','0','1'] or t=='NAND': continue
        if t[0].isupper():
            if not t in arrays: arrays.append(t)
        else:
            if not t in scalars: scalars.append(t)
    return scalars, arrays
    
class NANDTM:
   
        
    def _repr_pretty_(self, p, cycle):
        if cycle: return "cycle"
        print (self.source)
        
    def __init__(self, source):
        self.source = [l for l in source.split('\n') if l]
        self.scalars , self.arrays  =  extractvars(source)
        self.vals = collections.defaultdict(int)
        self.i = 0
        self.pc = 0
        self.maxlen = 1
        self.namelen = max([len(a) for a in self.scalars]+[len(a) for a in self.arrays])
        self.MAXSTEPS = 50
        self.modified = ()
        
    def getval(self,varname, i = 0):
        return self.vals[(varname,i)]
        
    def setval(self,varname,i,val):
        self.vals[(varname,i)] = val
        
    
    def input(self, x):
        for i,a in enumerate(x):
            self.setval("X",i,int(a))
            self.setval("X_nonblank",i,1)
        self.pc = 0
        self.i = 0
        self.maxlen = len(x)
    
    def modifiedvar(self):
        line = self.source[self.pc]
        if line[:9] == "MODANDJMP": return ("_",0)
        foo, op, bar, blah = parseline(line)
        if foo[-1]==']':
            j = foo.find("[")
            name_ = foo[:j]
            i_    = self.i if foo[j+1]=='i' else int(foo[j+1:-1])
        else:
            name_ = foo
            i_ = 0
        return name_,i_
    
    def printstate(self):
        res = ""
        def arrvals(name):
            def v(name,i):
                name_,i_ = self.modifiedvar()
                a = str(self.getval(name,i))
                if (name_,i_)==(name,i):
                    return mygreen(a)
                if self.i == i:
                    return myred(a)
                return a
            return "".join([v(name,i) for i in range(self.maxlen) ])
        name_,i_ = self.modifiedvar()
        
        for a in self.arrays:
            b = mygreen(a.ljust(self.namelen)) if a==name_ else a.ljust(self.namelen)
            res += b + ": "+ arrvals(a)+"\n"
        for a in self.scalars:
            b = mygreen(a.ljust(self.namelen)) if a==name_ else a.ljust(self.namelen)
            res += b + ": "+ str(self.getval(a))+"\n"
        res += "\n"
        for p,l in enumerate(self.source):
            if p == self.pc:
                l = myred(l)
            res += l+"\n"
        print(res)
    
    
    def next(self,printstate = False):
        def pname(foo):
            if foo[-1]==']':
                j = foo.find("[")
                name = foo[:j]
                i    = self.i if foo[j+1]=='i' else int(foo[j+1:-1])
            else:
                name = foo
                i = 0
            return name,i
        
        line = self.source[self.pc]
        if line[:9] == "MODANDJMP":
            j = line.find("(")
            k = line.find(",")
            l = line.find(")")
            a = self.getval(*pname(line[j+1:k].strip()))
            b = self.getval(*pname(line[k+1:l].strip()))
            if printstate:
                clear_output()
                self.printstate()
            if not a and not b: raise HaltExecution("halted")
            if b:
                if a: self.i += 1
                else: self.i = max(0,self.i-1)
            self.pc = 0
            self.maxlen = max(self.maxlen, self.i+1)
            return
        foo, op, bar, blah = parseline(line)
        a = self.getval(*pname(bar))
        b = self.getval(*pname(blah))
        self.setval(*pname(foo),1-a*b)
        self.pc = self.pc + 1 
        if printstate:
            clear_output()
            self.printstate()
    
    def run(self,iterate = False, maxsteps = 0):
        if iterate:
            print("q(uit), n(ext),p(rev),c(lear),r(un),s(kip) XX")
        if not maxsteps:
            maxsteps = self.MAXSTEPS
        t = 0
        noprinting = 0
        quit_cmd = False
        try:
            while True:
                if noprinting>0:
                    noprinting -= 1
                else:
                    clear_output()
                    self.printstate()
                if iterate and noprinting<=0:
                    cmd = input("")
                    #CURSOR_UP_ONE = '\x1b[1A'
                    #ERASE_LINE = '\x1b[2K'
                    #print(CURSOR_UP_ONE + ERASE_LINE + CURSOR_UP_ONE)
                    
                    c = cmd[0] if cmd else "n"
                    if c=="c":
                        clear_output()
                    elif c=="r":
                        iterate = False
                    elif c=="s":
                        _,num = cmd.split(' ')
                        print("...")
                        noprinting = int(num)
                    elif c=="p":
                        self.prev()
                        t -= 1
                        continue
                    elif c=="q":
                        raise QuitExecution("User quit")
                self.next()
                if t >= maxsteps:
                    raise Exception("Too many steps")
                t += 1
               
        except HaltExecution as e:
            msg = str(e)
            clear_output()
            self.printstate()
            y = ""
            i = 0
            while self.getval("Y_nonblank",i) :
                y += str(self.getval("Y",i))
                i += 1
            return y
        except  QuitExecution as e:
            print(str(e))
            
# own code now
# implementing AND(f1, f2).
# going to use f1 to equal or, and f2 to equal and

source = r'''
f_one_result = f1(X[i], f_one_result) 
f_two_result = f2(X[i], f_two_result)
intermediary = NAND(f_one_result, f_two_result)
Y[i] = NAND(intermediary, intermediary)
temp_for_constant = NAND(one_value, one_value) 
is_first = NAND(one_value, temp_for_constant)
constant_zero = NAND(is_first, is_first)
should_set_one = NAND(is_first, constant_zero)
y_nonblank_intermediary = NAND(should_set_one, Y_nonblank[i])
Y_nonblank[i] = NAND(y_nonblank_intermediary, y_nonblank_intermediary)
x_temp_was_at_end = NAND(x_was_at_end, x_was_at_end)
x_was_at_end = NAND( X_nonblank[i], x_was_at_end)
MODANDJUMP(x_was_at_end, y_nonblank_intermediary)'''

andprog = NANDTM(source)
andprog.input("111")
andprog.printstate()


'''


# the problem doesn't say we can use the constant one function as syntactic sugar,
# so we need to calculate it. We can NAND any value with itself, and then NAND that
# value with the original value to compute that. 
temp_for_constant = NAND(one_value, one_value) 
constant_one = NAND(one_value, temp_for_constant)
constant_zero = NAND(constant_one, constant_one)

should_set_one = NAND(is_first, constant_one)
is_first = constant_one

# end condition, we need to check if Y_nonblank is 1. Since we only set the first (zeroth)
# index to one, this condition will only occur when we return to the first index to place 
# the value of the final result.
y_check = Y_nonblank[i]

# we can always set the value of Y[i] equal to the current computed value, it will be
# overwritten on our return to the start with the final value and that is the only value
# that will be interpreted as the answer
Y[i] = and_result

# set the value of y_nonblank. We cannot simply set the value however. We need to check if
# we are on the return to the beginning. To do this, we can NAND y_check and should_set_one.
# both of these values will never be one. Only one of them will be equal to 1 at any given time
# so if we invert the result of the aforementioned NAND, we will get 0 when both are 0, as intended. We will get 1 when either value is 1, as intended as well. 
y_nonblank_intermediary = NAND(should_set_one, y_check)
y_nonblank_value = NAND(y_nonblank_intermediary, y_nonblank_intermediary)
Y_nonblank[i] = y_nonblank_value

# we want a value that will tell us if we have seen the end - to tell us to start going back
# until we reach the beginning of the array
x_nonblank = X_nonblank[i]
x_temp_was_at_end = NAND(x_was_at_end, x_was_at_end)
x_was_at_end = NAND(x_nonblank, x_was_at_end)

MODANDJUMP(x_was_at_end, y_non_blank_intermediary) # terminate when we reach the end of the inputs. '''