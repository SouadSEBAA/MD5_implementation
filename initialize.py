from math import *
from config import *

#1. initialize internal state
state_A = 0x67452301
state_B = 0xefcdab89
state_C = 0x98badcfe
state_D = 0x10325476

#2. initialize K
K = [int(2**32 * abs(sin(i))) & 0xffffffff for i in range(1,NUMBER_OP_PER_BLOCK+1)]
DEBUG and print(f"[+] This is K : {K}")

#3.1 initiliaze s to be used in each round
s = [[7, 12, 17, 22] * NUMBER_OP_PER_ROUND]
s += [[5, 9, 14, 20] * NUMBER_OP_PER_ROUND]
s += [[4, 11, 16, 23] * NUMBER_OP_PER_ROUND]
s += [[6, 10, 15, 21] * NUMBER_OP_PER_ROUND]

#3.2 initiliaze g to be used in each round
g = [[ i % 16 for i in range(NUMBER_OP_PER_ROUND) ]]
g += [[ (5*i + 1) % 16 for i in range(NUMBER_OP_PER_ROUND) ]]
g += [[ (3*i + 5) % 16 for i in range(NUMBER_OP_PER_ROUND) ]]
g += [[ (i*7) % 16 for i in range(NUMBER_OP_PER_ROUND) ]]