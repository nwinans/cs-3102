"""The first three functions are just used for testing purposes for this assignment. list_strings gives a list of all strings of length n, string_to_nat and nat_to_string convert back and forth between binary strings and natural numbers."""

def list_strings(n):
    """lists all binary strings of length n, do not modify this function"""
    if n == 0:
        return [""]
    else:
        strings = []
        for b in list_strings(n-1):
            strings.append(b+"0")
            strings.append(b+"1")
        return strings
        
def string_to_nat(b):
    """Given a binary string, converts it into a natural number.  Do not modify this function."""
    if b == "":
        return 0
    else:
        return 2 * string_to_nat(b[:-1]) + int(b[-1])
        

def nat_to_string(x):
    """Given a natural number, converts it into a binary string  Do not modify this function."""
    assert(x >= 0)
    if x == 0:
        return ""
    else:
        return nat_to_string(x//2) + str(x % 2)
        
"""This next block of functions is setting us up to program in AON-Straightline. The is_binary function checks that we are only computing on binary inputs/outputs (the only data type that AON-Straightlin can handle). The AND, OR, and NOT functions implement the corresponding boolean operators in python. """

def is_binary(b):
    return b == '1' or b == '0'

def AND(a,b):
    assert(is_binary(a) and is_binary(b))
    return str(int(a)*int(b))

def OR(a,b):
    assert(is_binary(a) and is_binary(b))
    return str(int(a)+int(b) - int(a)*int(b))

def NOT(a):
    assert(is_binary(a))
    return str(1-int(a))
    
"""Finally, from here we're programming in AON-Straightline. We start out by implementing some of the functions in class in AON-Straightline: XOR, NAND, and MAJ. These give you an idea for how AON-Straightline should be written (in general and by you in this assignment). Each line in the program should consist of a new variable declaration on the left-hand side and an AND/OR/NOT operation on the right-hand side, or else a return statement. Please note that you cannot use any operations besides AND/OR/NOT on the right-hand side (except for one case where you'll be directed otherwise), you cannot have multiple operations nested (e.g. NOT(AND(a,b)) is not permitted), and you cannot re-assign and already assigned variable (e.g. a = NOT(a) is not permitted)."""
    
def XOR(a,b):
    not_a = NOT(a)
    not_b = NOT(b)
    a_not_b = AND(a, not_b)
    b_not_a = AND(b, not_a)
    return OR(a_not_b, b_not_a)

def NAND(a,b):
    a_and_b = AND(a,b)
    return NOT(a_and_b)
    
def MAJ(a,b,c):
    assert(is_binary(a) and is_binary(b) and is_binary(c))
    first_two = AND(a,b)
    last_two = AND(b,c)
    first_last = AND(a,c)
    temp = OR(first_two, last_two)
    return OR(temp, first_last)

"""Uncomment the code block below to see XOR, NAND, and MAJ in action. Here we're enumerating all possible inputs and printing out each function's output for those inputs. This is also how the following asserts will test the code you write (except instead of printing it compares the output to the correct answers)."""
    
#for i in list_strings(2):
#    print('AND', i, AND(i[0], i[1]))
#for i in list_strings(2):
#    print('OR', i, OR(i[0], i[1]))
#for i in list_strings(2):
#    print('XOR', i, XOR(i[0], i[1]))
#for i in list_strings(2):
#    print('NAND', i, NAND(i[0], i[1]))
#for i in list_strings(3):
#    print('MAJ', i, MAJ(i[0], i[1], i[2]))



"""Now you're ready to start implementing programs in AON straightline for yourself. Implement the two functions (IMPL, COMPARE4) described below."""

def IMPL(a,b):
    not_a = NOT(a)
    not_b = NOT(b)
    
    and_not_not = AND(not_a, not_b)
    and_a_b = AND(a, b)
    xnor_a_b = OR(and_not_not, and_a_b)
    and_not_b = AND(not_a, b)
    return OR(xnor_a_b, and_not_b)

"""Checks that your implementation of IMPL is correct. It enumerates all inputs(note there are only finitely many, so we can be exhaustive), and checks the answer"""
assert(IMPL('0','0') == '1')
assert(IMPL('0','1') == '1')
assert(IMPL('1','0') == '0')
assert(IMPL('1','1') == '1')
print("IMPL works! Nicely, done!")
    
    
    
def COMPARE4(a0, a1, a2, a3, b0, b1, b2, b3):
    not_b0 = NOT(b0)
    not_b1 = NOT(b1)
    not_b2 = NOT(b2)
    not_b3 = NOT(b3)

    and_0 = AND(a0, not_b0)
    or_0  = OR(a0, not_b0)

    and_1 = AND(a1, not_b1)
    or_1 = OR(a1, not_b1)

    and_2 = AND(a2, not_b2)
    or_2 = OR(a2, not_b2)

    and_3 = AND(a3, not_b3)

    one_term = and_0

    and_or_and_0_1 = AND(or_0, and_1)

    two_term = OR(one_term, and_or_and_0_1)

    and_or_or_0_1 = AND(or_0, or_1)
    and_and_and_0_1_2 = AND(and_or_or_0_1, and_2)

    three_term = OR(two_term, and_and_and_0_1_2)

    and_and_or_0_1_2 = AND(and_or_or_0_1, or_2)
    and_and_and_0_1_2_3 = AND(and_and_or_0_1_2, and_3)

    four_term = OR(three_term, and_and_and_0_1_2_3)

    return four_term
    
"""Checks that your implementation of COMPARE4 is correct. It enumerates all inputs(note there are only finitely many, so we can be exhaustive), and checks the answer"""
for a in list_strings(4):
    for b in list_strings(4):
        na = string_to_nat(a) 
        nb = string_to_nat(b)
        if na > nb:
            assert(COMPARE4(a[0], a[1], a[2], a[3], b[0], b[1], b[2], b[3]) == '1')
        else:
            assert(COMPARE4(a[0], a[1], a[2], a[3], b[0], b[1], b[2], b[3]) == '0')
print("Great Scott, you got COMPARE4 working!!")



"""Now re-implement XOR in the NAND-Straightline language (follow the same rules as AON-Straightline, but only use the NAND operation on the right-hand side)."""
def XOR_nand(a, b):
    a_b = NAND(a, b)
    b_a_b = NAND(a_b, b)
    a_a_b = NAND(a_b, a)
    return NAND(b_a_b, a_a_b)

for i in list_strings(2):
    assert(XOR(i[0], i[1]) == XOR_nand(i[0], i[1]))