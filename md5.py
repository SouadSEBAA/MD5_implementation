#!/bin/python3
import binascii
from math import *
from bitarray import bitarray
import sys
from config import *
from initialize import *

def padd(m):
    padded_m = bitarray(endian='big') # i used bitarray structure
    padded_m.frombytes(m)

    # add bit 1
    padded_m.append(1)
    # fill the rest of as many 0s until length becomes congruent to 448 modulo 512
    while len(padded_m) % 512 != 448:
        padded_m.append(0)

    assert(len(padded_m) % 512 == 448)
    DEBUG and print(f"[+] padded message = {padded_m} \n len(m) % 512 = {len(m)%512}")
    
    # padd length of the message to it
    length_to_padd = padd_length(m)
    padded_m.extend(length_to_padd) 
    
    assert(len(padded_m) % 512 == 0)
    DEBUG and print(f"[+] added length to padded message {padded_m}")

    return padded_m

#2. append the length of m to the padded message
def padd_length(m):
    l = len(m)
    length_bitarray = bitarray(endian='big')
    length_bitarray.frombytes((l*8).to_bytes(8,byteorder='little')) # multiply l by 8 to produce length of m in bits not bytes (because l is length of m in bytes)
    return length_bitarray

# the hash function

def md5(m):
    # padd message
    padded_m = padd(m)

    #3. initialize variables
    A = state_A
    B = state_B
    C = state_C
    D = state_D
    
    # iterate over blocks of 64 bytes
    for j in range(len(padded_m)//512):
        #save regiters' value before strating this block, we need this value later
        AA = A
        BB = B
        CC = C
        DD = D

        #contruct M that splits the block into 16 words
        X = [padded_m[(j*512)+k:(j*512)+k+32] for k in range(0,512,32)] # X contains 16 chunks of 32 bits
        M = [int.from_bytes(x.tobytes(), byteorder='little') for x in X] # each chunk of X is turned into a decimal value, we note that we use it in little endian
        
        assert(len(M) == 16)
        DEBUG and print(f"[+] for the block {j}, M is {M}")

        #compute rounds
        for r in range(4):
            #do 16 operations in each round
            for op in range(16):
                v = function[r](B,C,D)
                v = add_modulo_2_32(v, A)
                v = add_modulo_2_32(v, M[g[r][op]])
                v = add_modulo_2_32(v, K[op+ 16*r])
                v = left_rotate(v, s[r][op]) #this an important step, it is responsible of assuring the avalanche effect, so that if two inputs differ by one bit, the hash produced is completely different
                v = add_modulo_2_32(v, B)

                A = D
                D = C
                C = B
                B = v

                DEBUG and print(f"round = {r} op = {op}: A = {A}, B = {B}, C = {C}, D = {D}, M[{g[r][op]}] = {M[g[r][op]]}, K[{op*(r+1)}] = {K[op*(r+1)]}, s[{r}][{op}] = {s[r][op]}")
        
        A = add_modulo_2_32(A, AA)
        B = add_modulo_2_32(B, BB) 
        C = add_modulo_2_32(C, CC)
        D = add_modulo_2_32(D, DD)

        assert(A<=0xffffffff and B<=0xffffffff and C<=0xffffffff and D<=0xffffffff)

    A = A.to_bytes(4, byteorder='little')
    B = B.to_bytes(4, byteorder='little')
    C = C.to_bytes(4, byteorder='little')
    D = D.to_bytes(4, byteorder='little')

    h = binascii.hexlify(A+B+C+D)
    return h

def main():
    m = sys.argv[1].encode()
    h = md5(m)
    print(f"[+] MD5 hash is {h}")

main()