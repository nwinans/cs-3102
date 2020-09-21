"""The first three functions are just used for testing purposes for this assignment. You also saw them in the last programming problem set. list_strings gives a list of all strings of length n, string_to_nat and nat_to_string convert back and forth between binary strings and natural numbers."""

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
    
"""FOr this assignment we're programming in NAND-Straightline in for some functions, and NAND-Straightline with sugar for others. We start out by implementing some of the functions in class in AON-Straightline: XOR, NAND, and MAJ (you saw these last week). Recall that each line in the program should consist of a new variable declaration on the left-hand side and a NAND operation (or the permitted sugary operation for some problems) on the right-hand side, or else a return statement. Please note that you cannot have multiple operations nested (e.g. NOT(AND(a,b)) is not permitted), and you cannot re-assign and already assigned variable (e.g. a = NOT(a) is not permitted)."""
    
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

"""For this assignment you'll be building arithmetic (specifically, addition) using straightline programs. Keep in mind that straightline programs can be easily converted into boolean gates, meaning that you're actually starting to build components of real integrated circuits here. How neat is that?!

These are going to be using a similar recursive definition of functions as what you saw with LOOKUP from lecture. You'll be able to build "larger" versions of functions out of smaller versions of the same functions.

To begin, we will implement a half adder. Sometimes when adding n-bit numbers together, the result will be n+1 bits long. Consider the sum (in binary) 10+11=101. A half adder is an adder which takes as input two n-bit natural numbers and returns the least significant n bits of their sum. For the previous example, a half-adder would return 01.

Implement a 2-bit half adder below. You may only use NAND
"""

def HADD2(a0, a1, b0, b1):
    a_b = NAND(a1, b1)
    nand_a_b = NAND(a1, a_b)
    nand_b_a = NAND(b1, a_b)
    s1 = NAND(nand_a_b, nand_b_a)
    c = NAND(a_b, a_b)

    a_nand_b = NAND(a0, b0)
    a_nand_nand_a = NAND(a0, a_nand_b)
    b_nand_nand_b = NAND(b0, a_nand_b)
    triple_nand = NAND(a_nand_nand_a, b_nand_nand_b)
    c_triple_nand = NAND(c, triple_nand)
    triple_nand_nand = NAND(triple_nand, c_triple_nand)
    c_nand_triple_nand = NAND(c, c_triple_nand)
    s = NAND(triple_nand_nand, c_nand_triple_nand)

    return s, s1

assert(HADD2('1','0','1','0') == ('0','0'))
assert(HADD2('1','1','1','0') == ('0','1'))
assert(HADD2('0','0','0','0') == ('0','0'))
assert(HADD2('1','1','0','1') == ('0','0'))

"""A Full Adder is a function that takes in three bits as input and gives their sum as output. For example, FADD(0,1,1) = 1,0. The idea of a full adder is that two of the bits will represent input bits in the addition, and the third bit will represent the carry value of the addition of a less-significant bit.

Implement a Full Adder below. You may use only NAND."""

def FADD(a,b,c):
    a_nand_b = NAND(a, b)
    a_nand_nand_a = NAND(a, a_nand_b)
    b_nand_nand_b = NAND(b, a_nand_b)
    triple_nand = NAND(a_nand_nand_a, b_nand_nand_b)
    c_triple_nand = NAND(c, triple_nand)
    triple_nand_nand = NAND(triple_nand, c_triple_nand)
    c_nand_triple_nand = NAND(c, c_triple_nand)
    s = NAND(triple_nand_nand, c_nand_triple_nand)
    c = NAND(c_triple_nand, a_nand_b)

    return c, s
    
assert(FADD("0","1","1") == ("1","0"))
assert(FADD('0','0','0') == ('0','0'))
assert(FADD('0','1','0') == ('0','1'))
assert(FADD('1','1','1') == ('1','1'))

"""Use the HADD2 and FADD procedures to implement a function that adds together two 4-bit numbers. You may use NAND, XOR, MAJ, or any other procedures as syntactic sugar if you wish (you must follow these same rules when implementing your own procedures)."""
def HADD1(a, b):
    a_b = NAND(a, b)
    nand_a_b = NAND(a, a_b)
    nand_b_a = NAND(b, a_b)
    s = NAND(nand_a_b, nand_b_a)
    c = NAND(a_b, a_b)
    return c, s


def ADD4(a0, a1, a2, a3, b0, b1, b2, b3):
    # compute each digit
    #carry3, least_sig = FADD(a3, b3, '0')
    carry3, least_sig = HADD1(a3, b3)
    carry2, second_least_sig = FADD(a2, b2, carry3)
    carry1, second_most_sig = FADD(a1, b1, carry2)
    carry0, most_sig = FADD(a0, b0, carry1)

    return carry0, most_sig, second_most_sig, second_least_sig, least_sig
    
assert(ADD4('0','0','0','0','1','1','1','1') == ('0','1','1','1','1'))
assert(ADD4('1','1','1','1','1','1','1','1') == ('1','1','1','1','0'))
assert(ADD4('1','0','1','0','0','1','0','1') == ('0','1','1','1','1'))
"""The next problem is a challenge problem. These are problems whose difficulty is so high that we do not necessarily expect most students will be able to do them within the time constraints of this assignment. We do, though, believe that they will be good practice. You are not required to complete or even attempt any challenge problems, but if you do, please let you Cohort Coach know. Successful completion of challenge problems will very much impress the course staff, and can also improve your community score.

CHALLENGE: Implement a function which computes the product of two 4-bit numbers"""

# Looking at binary mulitiplication, at the 1x1 level, it is essentially ANDing bits together since
# the result of two numbers multiplied in binary is only 1 when the two bits are 1. Thus, to perform
# grade school multiplication where we multiply one digit on the bottom row by the whole top row, save
# places and add, we can just create a new function to multiply a 4 digit number by a 1 digit number
# where we just AND all the values. 

def MULT41(a0, a1, a2, a3, b0):
    a_inv = NAND(a0, b0)
    b_inv = NAND(a1, b0)
    c_inv = NAND(a2, b0)
    d_inv = NAND(a3, b0)

    a = NAND(a_inv, a_inv)
    b = NAND(b_inv, b_inv)
    c = NAND(c_inv, c_inv)
    d = NAND(d_inv, d_inv)

    return a, b, c, d


def MULT4(a0, a1, a2, a3, b0, b1, b2, b3):
    # then to actually multiply a 4 digit number by another, we need to multiply each bit in b by all
    # the bits in a
    fourth_0, fourth_1, fourth_2, fourth_3 = MULT41(a0, a1, a2, a3, b3)
    third_0, third_1, third_2, third_3 = MULT41(a0, a1, a2, a3, b2)
    second_0, second_1, second_2, second_3 = MULT41(a0, a1, a2, a3, b1)
    first_0, first_1, first_2, first_3 = MULT41(a0, a1, a2, a3, b0)

    # then we need to add the bits together, saving the place of each corresponding partial product
    stage_2_0, stage_2_1, stage_2_2, stage_2_3, stage_2_4 = ADD4("0", fourth_0, fourth_1, fourth_2, third_0, third_1, third_2, third_3)
    stage_3_0, stage_3_1, stage_3_2, stage_3_3, stage_3_4 = ADD4(stage_2_0, stage_2_1, stage_2_2, stage_2_3, second_0, second_1, second_2, second_3)
    stage_4_0, stage_4_1, stage_4_2, stage_4_3, stage_4_4 = ADD4(stage_3_0, stage_3_1, stage_3_2, stage_3_3, first_0, first_1, first_2, first_3)

    # notice how in the result, the very last term is actually just from the product stage since no
    # other partial product can have that small of a significant value (only 1x1 can fill the 1's 
    # place in binary)
    return stage_4_0, stage_4_1, stage_4_2, stage_4_3, stage_4_4, stage_3_4, stage_2_4, fourth_3

assert(MULT4('1','1','1','1','1','1','0','0') == ('1','0','1','1','0','1','0','0')) # 15x12=180
assert(MULT4('1','0','1','0','1','0','1','1') == ('0','1','1','0','1','1','1','0')) # 10x11=110
assert(MULT4('0','0','0','0','1','1','1','1') == ('0','0','0','0','0','0','0','0')) # 15x0=0
assert(MULT4('1','1','1','1','1','1','1','1') == ('1','1','1','0','0','0','0','1')) #15x15=225
