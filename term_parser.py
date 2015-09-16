# parse terms

INFIX_OPERATORS = ["+", "-", "*", "/"]
PREFIX_OPERATORS = ["+", "-"]
OPERATORS = INFIX_OPERATORS

PREFERENCES = { "+": 1, "-": 1, "*": 2, "/": 2}

verbose = False

input = ""
pos = 0

def debug(message):
    if not verbose:
        return
    print(">>> ", message)

def setInput(text):
    global input
    global pos
    input = text
    pos = 0

def hasData():
    return pos < len(input)

def printPos():
    print(input)
    print(" " * pos + "^")
    
def getChar():
    if verbose:
        printPos()
    return input[pos]

def readChar():
    global pos
    c = getChar()
    pos = pos + 1
    # print(pos)
    return c

def skipWhitespace():
    while hasData() and getChar().isspace():
        readChar()

def readConstant():
    skipWhitespace()
    c = ""
    while hasData() and getChar().isdigit():
        c = c + readChar()
    return c    

def getPreference(operator):
    if len(operator) == 0:
        return 0
    return PREFERENCES[operator]

def readOperator():
    skipWhitespace()
    if not hasData():
        return ""
    c = getChar()
    if c in OPERATORS:
        readChar()
        return c
    return ""

def readBracketTerm():
    assert "(" == readChar(), "( expected"
    r = readMaximalTerm()
    debug("bracket result: " + str(r))
    skipWhitespace()        
    assert ")" == readChar(), ") expected"
    return r

def readMinimalTerm():
    skipWhitespace()
    if not hasData():
        return []
    c = getChar()
    r = ""
    if c == "(":
        r = readBracketTerm()
    elif c.isdigit():
        r = readConstant()
    return r
    
def readMaximalTerm():
    t1 = readMinimalTerm()
    op1 = readOperator()
    while len(op1) > 0:
        t2 = readMinimalTerm()
        assert len(t2) > 0
        op2 = readOperator()
        if len(op2) == 0:
            return [op1, t1, t2]
        if getPreference(op2) <= getPreference(op1):
            t1 = [op1, t1, t2]
            op1 = op2
        else:
            t3 = readMaximalTerm()
            assert len(t3) > 0
            return [op1, t1, [op2, t2, t3]]
    return t1

def createTerm(text):
    setInput(text)
    t = readMaximalTerm()
    print(t)
    printTerm(t)
    return t

def hasPrefixOperator(term):
    return len(term) == 2 and term[0] in PREFIX_OPERATORS

def term2str(term):
    r = ""
    if type(term) is list:
        if hasPrefixOperator(term):
            r = term[0]
            for t in term[1:]:
               r = r + term2str(t)
        else:
            r = "("
            for t in term[1:-1]:
               r = r + term2str(t)
               r = r + term[0]
            r = r + term2str(term[-1])   
            r = r + ")"
    else:           
        r = str(term)
    return r    

def printTerm(term):
    print(term2str(term))
    
#printTerm(createTerm("17 * 8"))

# Testing
def test(input, output):
    assert term2str(createTerm(input)) == output

test("17 * 8", "(17*8)")
test("((1-2))", "(1-2)")
test("71+2+3", "((71+2)+3)")
test("9   /3  ", "(9/3)")
test("1+2+3", "((1+2)+3)")
test("1-3+(7+9)", "((1-3)+(7+9))")
test("1-3+7+9", "(((1-3)+7)+9)")
test("1+3*7", "(1+(3*7))")
test("1*2+3*4","((1*2)+(3*4))")

createTerm("1+2+3+4")     
