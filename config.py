DEBUG = True
NUMBER_OP_PER_ROUND = 16
NUMBER_ROUNDS = 4
NUMBER_OP_PER_BLOCK = NUMBER_OP_PER_ROUND * NUMBER_ROUNDS

F = lambda x,y,z: (x & y) | (~x & z)
G = lambda x,y,z: (x & z) | (y & ~z)
H = lambda x,y,z: x ^ y ^ z
I = lambda x,y,z: y ^ (x | ~z)
left_rotate = lambda x,n: (((x << n) | (x >> (32 - n))) & (0xffffffff))
add_modulo_puiss_2 = lambda a,b,n: (a+b) & int('ff'*(n//8), 16)
add_modulo_2_32 = lambda a,b: add_modulo_puiss_2(a,b,32)


function = {0: F, 1:G, 2:H, 3:I}


''' F(X,Y,Z) = XY v not(X) Z
    G(X,Y,Z) = XZ v Y not(Z)
    H(X,Y,Z) = X xor Y xor Z
    I(X,Y,Z) = Y xor (X v not(Z))'''