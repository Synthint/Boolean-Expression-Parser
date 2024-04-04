

class Token:
    right = None
    left = None
    state = None
    
    def __init__(self,kind ,value, priority):
        self.kind = kind
        self.value = value
        self.priority = priority
    def __str__(self):
        return self.value
    def giveChildren(self,left,right):
        self.left = left
        self.right = right
    def setState(state):
        self.state = state
    
 

def tokenize(string):
    string = string.upper()
    stream = []
    for x in range(len(string)):
        if string[x] in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            stream.append(Token("var",string[x],None))
            if x<len(string)-1 and string[x+1] in "(ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                stream.append(Token("and","*",2))
            
                
        elif string[x] in "*":
             stream.append(Token("and","*",2))
                           
        elif string[x] in "+":
             stream.append(Token("or","+",1))
                           
        elif string[x] in "'":
             stream.append(Token("not","'",5))
             if x<len(string)-1 and string[x+1] in "(ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                 stream.append(Token("and","*",2))

        elif string[x] in "(":
             stream.append(Token("lparen","(",0))

        elif string[x] in ")":
             stream.append(Token("rparen",")",None))
             if x<len(string)-1 and string[x+1] in "(ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                 stream.append(Token("and","*",2))
        elif string[x] in " ":
            continue
        else:
            raise ValueError('invalid symbol')

    return stream


        
    
def postfix(tokens):
    stack = []
    output = []

    for i in range(len(tokens)):
        if tokens[i].kind == "var":
            output.append(tokens[i])
        elif tokens[i].kind == "lparen":
            
            
            stack.append(tokens[i])
        elif tokens[i].kind == "and" or tokens[i].kind == "or" or tokens[i].kind == "not":
           
                
            
            if len(stack) == 0 or stack[-1].priority <= tokens[i].priority:
                stack.append(tokens[i])
            else:
                output.append(stack.pop())
                stack.append(tokens[i])
        elif tokens[i].kind == "rparen":
            while len(stack) > 0 and stack[-1].kind != "lparen":
                
                output.append(stack.pop())
            if len(stack)>0:
                stack.pop()
    while len(stack) != 0:
        output.append(stack.pop())
    return output
        
                
            
def makeAST(tokens):
    stack = []
    for tok in tokens:
        if tok.kind == "var":
            stack.append(tok)
        if tok.kind == "and" or tok.kind == "or":
            tok.giveChildren(stack.pop(),stack.pop())
            stack.append(tok)
        if tok.kind == "not":
            tok.giveChildren(stack.pop(),None)
            stack.append(tok)
    return stack[0]


def traverseAST(node):
    if node.left != None and node.right != None:
        return "("+traverseAST(node.left) + node.value+ traverseAST(node.right)+")"
    elif node.left != None:
        return "("+traverseAST(node.left) + node.value+")"
    else:
        return node.value
    
    
def traverseASTExcelOutput(node):
    if node.kind == "and":
        return "AND("+traverseASTExcelOutput(node.left) + "," + traverseASTExcelOutput(node.right)+")"
    elif node.kind == "or":
        return "OR("+traverseASTExcelOutput(node.left) + "," + traverseASTExcelOutput(node.right)+")"
    elif node.kind == "not":
        return "NOT("+traverseASTExcelOutput(node.left)+")"
    else:
        return node.value+"1"





def makeTruthTable(stack):
    output = []
    variables =  []
    for tok in stack:
        if tok.kind == "var":
            alreadyIn = False
            for var in variables:
                if tok.value == var:
                    alreadyIn = True
            if not alreadyIn:
                variables.append(tok.value)
    possibleCombos = 2**len(variables)
    
    combos = []
    for x in range(possibleCombos):
        num = str(bin(x)[2:].zfill(len(variables)))
        combos.append(num)
        
    variables = sorted(variables)
    labels = "".join(variables)
    labels = labels + " = Ouput"
    output.append(labels)
    for c in combos:
        tempStack = []
        for tok in stack:
            tempStack.append(tok)
        for t in range(len(tempStack)):
            for v in range(len(variables)):
                if tempStack[t].value == variables[v]:
                    tempStack[t].state = c[v]
                    
        tempAST = makeAST(tempStack)
        out = evaluateAST(tempAST)
        inStr = "".join(c)
        #print(traverseASTExcelOutput(tempAST))
        output.append(inStr + " = " + str(out))
    return output


        

def evaluateAST(ast):
    if ast.kind == "and":
        if evaluateAST(ast.left) == "1" and evaluateAST(ast.right) == "1":
            return "1"
        return "0"
    elif ast.kind == "or":
        if evaluateAST(ast.left) == "1" or evaluateAST(ast.right) == "1":
            return "1"
        return "0"
    elif ast.kind == "not":
        if evaluateAST(ast.left) == "1":
            return "0"
        return "1"
    else:
        return ast.state
        
                     
             
                

            
##    for tok in tokens:
##        if tok.kind == "var":
##            stack.append(tok)
##        if tok.kind == "and" or tok.kind == "or":
##            tok.giveChildren(stack.pop(),stack.pop())
##            stack.append(tok)
##        if tok.kind == "not":
##            tok.giveChildren(stack.pop(),None)
##            stack.append(tok)
    

print("""This is a boolean expression parser,
input any single letter variables and the operators
+,*, and ' to make an expression. The Parser is case insensitive.

Outputs truth table and excel formula for 
transferring a boolean expression easily into excel.
""")




x = input(">> ")
tokens = tokenize(x)
expr = postfix(tokens)
ast = makeAST(expr)
truthTable = makeTruthTable(expr)
##print(truthTable)
for tok in truthTable:
    print(tok)#.value)




print("\n EXCEL OUTPUT BELOW:")

print(traverseASTExcelOutput(ast))
    
    

input("press enter to exit ")





