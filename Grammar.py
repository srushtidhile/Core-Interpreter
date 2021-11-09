from Core import Core
from Scanner import Scanner
import sys

# Data Structures for Interpreter

intID = [] # tracking int types list
refID = [] # tracking ref types list

static = {} # global variables map
scope = [] # local variables stack of maps
refHeap = [] # ref type actual data storage heap

class Prog:

    def parse(self, S):
        self.ds = None

        if S.currentToken() != Core.PROGRAM:
            print("ERROR: Expected", Core.PROGROM.name)
            sys.exit()
        S.nextToken() #consume "program"

        # Parsing <decl-seq>
        if S.currentToken() != Core.BEGIN:
            self.ds = DeclSeq()
            self.ds.parse(S)

        # If DeclSeq not present, checking for expected "begin"
        if S.currentToken() != Core.BEGIN:
            print("ERROR: Expected", Core.BEGIN.name)
            sys.exit()
        S.nextToken() # consume "begin"

        # Parsing <stmt-seq>
        self.ss = StmtSeq()
        self.ss.parse(S)

        if S.currentToken() != Core.END:
            print("ERROR: Expected", Core.END.name)
            sys.exit()
        S.nextToken() # consume "end"

        if S.currentToken() != Core.EOF:
            print("ERROR: Expected", Core.EOF.name)
            sys.exit()

    def print(self):
        print ("program")
        if self.ds is not None:
            self.ds.print()
        print ("begin")
        self.ss.print()
        print ("end")

    def execute(self, D):
        if self.ds is not None:
            self.ds.execute(D)

        scope.append({}) # add scope
        self.ss.execute(D)
        scope.pop() # pop scope

class DeclSeq:
    def parse(self, S):

        # Parsing <decl>
        self.decl = Decl()
        self.decl.parse(S)
        self.decl_next = None

        # Parsing <decl-seq>
        if S.currentToken() != Core.BEGIN:
            self.decl_next = DeclSeq()
            self.decl_next.parse(S)

    def print(self):
        self.decl.print()
        if self.decl_next is not None:
            self.decl_next.print()

    def execute(self, D):
        typeScope = 0 # typeScope is global (0) because <decl> will be accessed through <decl-seq>
        self.decl.execute(D, typeScope)

        if self.decl_next is not None:
            self.decl_next.execute(D)

class StmtSeq:
    def parse(self, S):

        # Parsing <stmt>
        self.stmt = Stmt()
        self.stmt.parse(S)
        self.stmt_next = None

        # Checking if StmtSeq exists, and Parsing StmtSeq <stmt-seq>
        if S.currentToken() != Core.END and S.currentToken() != Core.ENDIF and S.currentToken() != Core.ELSE and S.currentToken() != Core.ENDWHILE:
            self.stmt_next = StmtSeq()
            self.stmt_next.parse(S)

    def print(self):
        self.stmt.print()
        if self.stmt_next is not None:
            self.stmt_next.print()

    def execute(self, D):
        self.stmt.execute(D)

        if self.stmt_next is not None:
            self.stmt_next.execute(D)

class Decl:
    def parse(self, S):
        self.decl = None
        
        # Calling DeclInt if int or Calling DeclClass if ref is current token; <decl-int> | <decl-class>
        if S.currentToken() == Core.INT:
            self.decl = DeclInt()
            self.decl.parse(S)
        elif S.currentToken() == Core.REF:
            self.decl = DeclClass()
            self.decl.parse(S)
        # If "int" or "ref" not found, display current token and exit
        else: 
            print("Error: Expected INT or REF, instead got ", S.currentToken().name)
            sys.exit()
    
    def print(self):
        self.decl.print()

    def execute(self, D, typeScope):
        if self.decl is not None:
            self.decl.execute(D, typeScope)

class DeclInt:
    def parse(self, S):

        if S.currentToken() != Core.INT:
            print("ERROR: Expected ", Core.INT.name)
            sys.exit()
        S.nextToken() # consume "int"

        # Parsing <id-list>
        self.list = IdList()
        self.list.parse(S)

        if S.currentToken() != Core.SEMICOLON:
            print("ERROR: Expected ", Core.SEMICOLON.name)
            sys.exit()
        S.nextToken() # consume ";"

    def print(self):
        print("int ", end = "")
        self.list.print()
        print(";")

    def execute(self, D, typeScope):
        typeVar = 0 # type = int/0
        self.list.execute(D, typeVar, typeScope)

class DeclClass:
    def parse(self, S):

        if S.currentToken() != Core.REF:
            print("ERROR: Expected ", Core.REF.name)
            sys.exit()
        S.nextToken() # consume "ref"

        # Parsing <id-list>
        self.list = IdList()
        self.list.parse(S)

        if S.currentToken() != Core.SEMICOLON:
            print("ERROR: Expected ", Core.SEMICOLON.name)
            sys.exit()
        S.nextToken() # consume ";"

    def print(self):
        print("ref ", end = "")
        self.list.print()
        print(";")

    def execute(self, D, typeScope):
        typeVar = 1 # type = ref/1
        self.list.execute(D, typeVar, typeScope)

class IdList:
    def parse(self, S):
        self.list = None
        self.option = 0

        if S.currentToken() != Core.ID:
            print("ERROR: Expected ", Core.ID.name)
            sys.exit()
        self.var = S.getID() # store variable name
        S.nextToken() # consume id

        # Checking for <id-list>, and Parsing <id-list>
        if S.currentToken() == Core.COMMA:
            self.option = 1
            S.nextToken() # consume ","
            self.list = IdList()
            self.list.parse(S)
    
    def print(self):
        print(self.var, end = "")
        if self.option == 1:
            print(",", end = "")
            self.list.print()

    def execute(self, D, typeVar, typeScope):
        
         # Global scope 
        if typeScope == 0:
            if typeVar == 0: # int type
                intID.append(self.var)
                static[self.var] = 0
            elif typeVar == 1: # ref type
                refID.append(self.var)
                static[self.var] = None

        # Local scope
        elif typeScope == 1:
            if typeVar == 0: # int type
                intID.append(self.var)
                # add to the map on the top of stack
                topIndex = len(scope) - 1
                scope[topIndex].update({self.var: 0})
            elif typeVar == 1: # ref type
                refID.append(self.var)
                # add to the map on the top of stack
                topIndex = len(scope) - 1
                scope[topIndex].update({self.var: None})

        # if self.list is not None self.list.execute()
        if self.option == 1:
            self.list.execute(D, typeVar, typeScope)

class Stmt:
    def parse(self, S):
        self.stmt_next = None
        self.typeScope = 0

        # Checking and Parsing <assign> | <if> | <loop> | <in> | <out> | <decl>
        if S.currentToken() == Core.ID:
            self.stmt_next = Assign()
            self.stmt_next.parse(S)
        elif S.currentToken() == Core.IF:
            self.stmt_next = If()
            self.stmt_next.parse(S)
        elif S.currentToken() == Core.WHILE:
            self.stmt_next = Loop()
            self.stmt_next.parse(S)
        elif S.currentToken() == Core.INPUT:
            self.stmt_next = Input()
            self.stmt_next.parse(S)
        elif S.currentToken() == Core.OUTPUT:
            self.stmt_next = Output()
            self.stmt_next.parse(S)
        elif S.currentToken() == Core.INT or S.currentToken() == Core.REF:
            self.typeScope = 1 # typeScope = local/1
            self.stmt_next = Decl()
            self.stmt_next.parse(S)
        # If none of the above tokens found, display invalid token and exit
        else:
            print("ERROR: Invalid token ", S.currentToken().name)
            sys.exit()

    def print(self):
        self.stmt_next.print()

    def execute(self, D):
        if self.typeScope == 1:
            self.stmt_next.execute(D, 1) # sent 1 which means local scope <decl>
        else:
            self.stmt_next.execute(D)

class Assign:
    def parse(self, S):
        self.e = None
        self.refVar = None
        self.option = 0

        if S.currentToken() != Core.ID:
            print("ERROR: Expected ", Core.ID.name)
            sys.exit()
        self.var = S.getID() # store variable name
        S.nextToken() # consume id

        if S.currentToken() != Core.ASSIGN:
            print("ERROR: Expected ", Core.ASSIGN.name)
            sys.exit()
        S.nextToken() # consume "="

        # Checking for either "new" or "ref" or <expr>
        if S.currentToken() == Core.NEW:
            self.option = 1
            S.nextToken() #consume "new"
        elif S.currentToken() == Core.REF:
            self.option = 2
            S.nextToken() #consume "ref"
            self.refVar = S.getID() # store variable name for ref
            S.nextToken() #consume id
        # Parsing <expr>
        else:
            self.e = Expr()
            self.e.parse(S)

        if S.currentToken() != Core.SEMICOLON:
            print("ERROR: Expected ", Core.SEMICOLON.name)
            sys.exit()
        S.nextToken() # consume ";"

    def print(self):
        print(self.var, end = "")
        print("=", end = "")
        if self.option == 0:
            self.e.print()
            print(";")
        elif self.option == 1:
            print("new", end = "")
            print(";")
        elif self.option == 2:
            print("ref ", end = "")
            print(self.refVar + ";")

    def execute(self, D):

        # int type
        if self.var in intID:
            if self.option == 0: # id = <expr>
                value = self.e.execute(D)
                # set self.var (key) to value (value)
                # check in last to first scope
                updated = False
                i = len(scope) - 1
                while i >= 0:
                    if self.var in scope[i]:
                        scope[i].update({self.var: value})
                        updated = True
                        break
                    i = i - 1
                # else check in global
                if updated == False:
                    if self.var in static:
                        static.update({self.var: value})

        # ref type
        elif self.var in refID:
            if self.option == 0: # id = <expr>
                value = self.e.execute(D)
                # get self.var(key)'s value in scope and use that as index into heap to change (value)
                # check in last to first scope
                updated = False
                i = len(scope) - 1
                while i >= 0:
                    if self.var in scope[i]:
                        index = scope[i].get(self.var)
                        refHeap[index] = value
                        updated = True
                        break
                    i = i - 1
                # else check in global
                if updated == False:
                    if self.var in static:
                        index = static.get(self.var)
                        refHeap[index] = value

            elif self.option == 1: # id = new
                # new index into heap as 0
                # check in last to first scope
                updated = False
                i = len(scope) - 1
                while i >= 0:
                    if self.var in scope[i]:
                        refHeap.append(0) # add a new position on the heap
                        index = len(refHeap) - 1
                        scope[i].update({self.var: index}) # add index as variable value
                        updated = True
                        break
                    i = i - 1
                # else check in global
                if updated == False:
                    if self.var in static:
                        refHeap.append(0) # add a new position on the heap
                        index = len(refHeap) - 1
                        static.update({self.var: index}) # add index as variable value
                    
            elif self.option == 2: # id = ref id
                # get self.refVar(key)'s value in scope or global
                updated = False
                i = len(scope) - 1
                while i >= 0:
                    if self.refVar in scope[i]:
                        index = scope[i].get(self.refVar)
                        updated = True
                        break
                    i = i - 1
                # else check in global
                if updated == False:
                    if self.refVar in static:
                        index = static.get(self.refVar)

                # put index into self.var's value
                updated2 = False
                j = len(scope) - 1
                while j >= 0:
                    if self.var in scope[j]:
                        scope[j].update({self.var: index})
                        updated2 = True
                        break
                    j = j - 1
                # else check in global
                if updated2 == False:
                    if self.var in static:
                        static.update({self.var: index})
        
class Input:
    def parse(self, S):

        if S.currentToken() != Core.INPUT:
            print("ERROR: Expected ", Core.INPUT.name)
            sys.exit()
        S.nextToken() # consume "input"
        self.var = S.getID() # store variable name
        S.nextToken() # consume id
        S.nextToken() # consume ";"

    def print(self):
        print("input ", end = "")
        print(self.var + ";")

    def execute(self, D):
        # if D.currentToken() == Core.EOF:
        #     print("ERROR: No data to read from input file")
        #     sys.exit()

        inputValue = D.getCONST()
        D.nextToken()
        # set self.var (key) to inputValue (value)
        # check in last to first scope
        updated = False
        i = len(scope) - 1
        while i >= 0:
            if self.var in scope[i]:
                scope[i].update({self.var: inputValue})
                updated = True
                break
            i = i - 1
        # else check in global
        if updated == False:
            if self.var in static:
                static.update({self.var: inputValue})

class Output:
    def parse(self, S):

        # Checking for expected "output"
        if S.currentToken() != Core.OUTPUT:
            print("ERROR: Expected ", Core.OUTPUT.name)
            sys.exit()
        S.nextToken() # consume "output"

        # Parsing <expr>
        self.e = Expr()
        self.e.parse(S)
        S.nextToken() # consume ";"

    def print(self):
        print("output ", end = "")
        self.e.print()
        print(";")

    def execute(self, D):
        value = self.e.execute(D)
        print(value) # print output

class If:
    def parse(self, S):
        self.ss2 = None
        self.option = 0

        # Checking for expected "if"
        if S.currentToken() != Core.IF:
            print("ERROR: Expected ", Core.IF.name)
            sys.exit()
        S.nextToken() # consume "if"

        # Parsing <cond>
        self.cond = Cond()
        self.cond.parse(S)
        
        # Checking for expected "then"
        if S.currentToken() != Core.THEN:
            print("ERROR: Expected ", Core.THEN.name)
            sys.exit()
        S.nextToken() # consume "then"

        # Parsing <stmt-seq>
        self.ss = StmtSeq()
        self.ss.parse(S)

        # Checking for expected "endif" or "else"
        if S.currentToken() != Core.ENDIF and S.currentToken() != Core.ELSE:
            print("ERROR: Expected ", Core.ENDIF.name, " or ", Core.ELSE.name)
            sys.exit()
        
        # If "endif" token found
        if S.currentToken() == Core.ENDIF:
            S.nextToken() # consume "endif"
        # If "else" token found, Parsing <stmt-seq>
        elif S.currentToken() == Core.ELSE:
            S.nextToken() # consume "else"
            self.option = 1
            self.ss2 = StmtSeq()
            self.ss2.parse(S)

            # Checking for expected "endif"
            if S.currentToken() != Core.ENDIF:
                print("ERROR: Expected ", Core.ENDIF.name)
                sys.exit()
            S.nextToken() # consume "endif"
    
    def print(self):
        print("if ", end = "")
        self.cond.print()
        print(" then")
        self.ss.print()
        if self.option == 0:
            print("endif")
        elif self.option == 1:
            print("else")
            self.ss2.print()
            print("endif")

    def execute(self, D):
        # Executing if <cond> then <stmt-seq> endif
        if self.option == 0:
            if self.cond.execute(D):
                scope.append({})  # add scope
                self.ss.execute(D)
                scope.pop() # pop scope

        # Executing if <cond> then <stmt-seq> else <stmt-seq> endif
        elif self.option == 1:
            if self.cond.execute(D):
                scope.append({}) # add scope
                self.ss.execute(D)
                scope.pop() # pop scope
            else:
                scope.append({}) # add scope
                self.ss2.execute(D)      
                scope.pop() # pop scope


class Loop:
    def parse(self, S):

        if S.currentToken() != Core.WHILE:
            print("ERROR: Expected ", Core.WHILE.name)
            sys.exit()
        S.nextToken() # consume "while"
        
        # Parsing <cond>
        self.cond = Cond()
        self.cond.parse(S)

        if S.currentToken() != Core.BEGIN:
            print("ERROR: Expected ", Core.BEIN.name)
            sys.exit()
        S.nextToken() # consume "begin"

        # Parsing <stmt-seq>
        self.ss = StmtSeq()
        self.ss.parse(S)

        if S.currentToken() != Core.ENDWHILE:
            print("ERROR: Expected ", Core.ENDWHILE.name)
            sys.exit()
        S.nextToken() # consume "endwhile"
    
    def print(self):
        print("while ", end = "")
        self.cond.print()
        print(" begin")
        self.ss.print()
        print("endwhile")

    def execute(self, D):
        # Executing while <cond> begin <stmt-seq> endwhile
        scope.append({}) # add scope
        while self.cond.execute(D):
            self.ss.execute(D)
        scope.pop() # pop scope

class Cond:
    def parse(self, S):
        self.cmpr = None
        self.cond = None
        self.option = 0

        # Parsing <cond> from !(<cond>)
        if S.currentToken() == Core.NEGATION:
            S.nextToken() # consume "!"
            S.nextToken() # consume "("
            self.cond = Cond()
            self.cond.parse(S)
            S.nextToken() # consume ")"
        # Parsing <cmpr>
        else:
            self.option = 1
            self.cmpr = Cmpr()
            self.cmpr.parse(S)
            # Parsing <cond> from <cmpr> or <cond>
            if S.currentToken() == Core.OR:
                S.nextToken() # consume "or"
                self.option = 2
                self.cond = Cond()
                self.cond.parse(S)
    
    def print(self):
        if self.option == 0:
            print("!", end = "")
            print("(", end = "")
            self.cond.print()
            print(")")
        elif self.option == 1:
            self.cmpr.print()
        elif self.option == 2:
            self.cmpr.print()
            print(" or ", end = "")
            self.cond.print()

    def execute(self, D):
        condition = False

        # Executing !(<cond>)
        if self.option == 0:
            condition = self.cond.execute(D)
            if condition is True:
                condition = False
            elif condition is False:
                condition = True
        # Executing <cmpr>
        elif self.option == 1:
            condition = self.cmpr.execute(D)
        # Executing <cmpr> or <cond>
        elif self.option == 2:
            valueCmpr = self.cmpr.execute(D)
            valueCond = self.cond.execute(D)
            if valueCmpr or valueCond:
                condition = True

        return condition

class Cmpr:
    def parse(self, S):

        # Parsing <expr>
        self.e1 = Expr()
        self.e1.parse(S)
        self.option = 0
        
        # Checking for "==" or "<" or "<="
        if S.currentToken() == Core.EQUAL:
            self.option = 0
            S.nextToken() # consume "=="
        elif S.currentToken() == Core.LESS:
            self.option = 1
            S.nextToken() # consume "<"
        elif S.currentToken() == Core.LESSEQUAL:
            self.option = 2
            S.nextToken() # consume "<="

        # Parsing <expr>
        self.e2 = Expr()
        self.e2.parse(S)

    def print(self):
        self.e1.print()
        if self.option == 0:
            print("==", end = "")
        elif self.option == 1:
            print("<", end = "")
        elif self.option == 2:
            print("<=", end = "")
        self.e2.print()
    
    def execute(self, D):
        comparison = False
        value1 = self.e1.execute(D)
        value2 = self.e2.execute(D)

        if self.option == 0:
            if value1 == value2: # <expr> == <expr>
                comparison = True
        elif self.option == 1:
            if value1 < value2: # <expr> < <expr>
                comparison = True
        elif self.option == 2:
            if value1 <= value2: # <expr> <= <expr>
                comparison = True
        return comparison

class Expr:
    def parse(self, S):
        self.e = None
        self.option = 0

        # Parsing <term>
        self.t = Term()
        self.t.parse(S)

        # Checking and Parsing for + <expr> or - <expr>
        if S.currentToken() == Core.ADD:
            S.nextToken() # consume "+"
            self.e = Expr()
            self.e.parse(S)
            self.option = 1
        elif S.currentToken() == Core.SUB:
            S.nextToken() # consume "-"
            self.e = Expr()
            self.e.parse(S)
            self.option = 2
    
    def print(self):
        self.t.print()
        if self.option == 1:
            print ("+", end = "")
            self.e.print()
        elif self.option == 2:
            print("-", end = "")
            self.e.print()

    def execute(self, D):
        # Executing <term>
        value = self.t.execute(D)

        if self.option == 1:
            value = value + self.e.execute(D) # <term> + <expr>
        elif self.option == 2:
            value = value - self.e.execute(D) # <term> - <expr>

        return value

class Term:
    def parse(self, S):
        self.t = None
        self.option = 0

        # Parsing <factor>
        self.f = Factor()
        self.f.parse(S)

        # Checking and Parsing for * <term>
        if S.currentToken() == Core.MULT:
            S.nextToken() # consume "*"
            self.t = Term()
            self.t.parse(S)
            self.option = 1

    def print(self):
        self.f.print()
        if self.option == 1:
            print("*", end = "")
            self.t.print()

    def execute(self, D):
        # Executing <factor>
        value = self.f.execute(D)
        # Executing <factor> * <term>
        if self.option == 1:
            value = value * self.t.execute(D)
        return value

class Factor:
    def parse(self, S):
        self.e = None
        self.var_id = None
        self.var_const = None

        # Checking for id or const or <expr>
        if S.currentToken() == Core.ID:
            self.var_id = S.getID() # store variable name
            S.nextToken() # consume id
        elif S.currentToken() == Core.CONST:
            self.var_const = S.getCONST() # store constant value
            S.nextToken() # consume const
        elif S.currentToken() == Core.LPAREN:
            S.nextToken() # consume (
            # Parsing <expr>
            self.e = Expr()
            self.e.parse(S)
            S.nextToken() # consume )

    def print(self):
        if self.var_id is not None:
            print(self.var_id, end = "")
        elif self.var_const is not None:
            print(self.var_const, end = "")
        elif self.e is not None:
            print("(", end = "")
            self.e.print()
            print(")")

    def execute(self, D):
        value = None

        if self.var_id is not None:
            if self.var_id in intID: # int type
                # find value from self.var (key)
                # check in last to first scope
                updated = False
                i = len(scope) - 1
                while i >= 0:
                    if self.var_id in scope[i]:
                        value = scope[i].get(self.var_id)
                        updated = True
                        break
                    i = i - 1
                # else check in global
                if updated == False:
                    if self.var_id in static:
                        value = static.get(self.var_id)

            elif self.var_id in refID: # ref type
                # find value from self.var (key), then get value from heap
                # check in last to first scope
                updated = False
                i = len(scope) - 1
                while i >= 0:
                    if self.var_id in scope[i]:
                        index = scope[i].get(self.var_id)
                        value = refHeap[index]
                        updated = True
                        break
                    i = i - 1
                # else check in global
                if updated == False:
                    if self.var_id in static:
                        index = static.get(self.var_id)
                        value = refHeap[index]

        elif self.var_const is not None: # const
            value = int(self.var_const)

        # Executing <expr>
        elif self.e is not None:
            value = self.e.execute(D)
        return value
