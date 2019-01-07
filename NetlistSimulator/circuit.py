'''
Input: Please modify the argument from 1 to 3, like "python circuit.py 1" 
    filename = 
        "netlist_1"
        "netlist_2a"
        "netlist_2b"
    ori_N = 
        7
        4
        3
Output: Voltage level of each bias points will be displayed.

Problem 1&4:
    For Problem 1, see "netlist_1"
    For Problem 4, see "netlist_2a" and "netlist_2b"

Note: The naming rule of dependent components is referencing:
    https://www.macspice.com/ug/sec3.html#s3.2.2.1

    Current-Dependent Current Sources : F-elements
    Voltage-Controlled Current Source : G-elements 

For mapping of bias points, please reference "circuit_bias_points.pdf"

Problem 2&5:
Please run the this Python code and see the result, note that we should modify the value of "testcase" for corresponding:
    1. filename: To the netlist file
    2. ori_N: The total number of bias points

For following MacSpice simulation, please also reference "MacSpice_1.pdf", "MacSpice_2a.pdf", and "MacSpice_2b.pdf"

Problem 3:
As I verify netlist part 1 with MacSpice, my spice file is "netlist_1_spice"
    MacSpice 3 -> print v(1) v(2) v(3) v(4) v(5) v(6) v(7)
    v(1) =  5.00000e+00 
    v(2) =  3.72549e+00 
    v(3) =  3.43137e+00 
    v(4) =  2.74510e+00 
    v(5) =  2.25490e+00 
    v(6) =  1.56863e+00 
    v(7) =  1.27451e+00

Which is similar to my result for netlist_1
Bias voltage at point 1 equals 4.999999999999998 volts
Bias voltage at point 2 equals 3.725490196078431 volts
Bias voltage at point 3 equals 3.4313725490196076 volts
Bias voltage at point 4 equals 2.7450980392156863 volts
Bias voltage at point 5 equals 2.2549019607843137 volts
Bias voltage at point 6 equals 1.5686274509803924 volts
Bias voltage at point 7 equals 1.2745098039215688 volts

Problem 6A:
As I verify netlist part 4A with MacSpice, my spice file is "netlist_2a_spice"
    MacSpice 3 -> print v(1) v(2) v(3) v(4)
    v(1) =  1.20000e+01
    v(2) =  1.80000e+01
    v(3) =  1.80000e+01
    v(4) = -6.00001e+00

Which is similar to my result for netlist_2a: 
Bias voltage at point 1 equals 12.0 volts
Bias voltage at point 2 equals 17.99999999900254 volts
Bias voltage at point 3 equals 17.99999999900254 volts
Bias voltage at point 4 equals -5.999999999238614 volts

## Special Note: In netlist_2a_spice, since the F element requires source device but not controlling nodes. For convenience I use voltage control current source instead and the parameter is 4/0.0001 = 4000.

Problem 6B:
As I verify netlist part 4B with MacSpice, my spice file is "netlist_2b_spice"
    MacSpice 3 -> print v(1) v(2) v(3)
    v(1) =  2.00000e+00 
    v(2) =  4.00000e+00 
    v(3) =  4.00000e+00 

Which is similar to my result for netlist_2b:
Bias voltage at point 1 equals 2.0000000000000004 volts
Bias voltage at point 2 equals 4.000000000000001 volts
Bias voltage at point 3 equals 4.000000000000001 volts

'''

import sys
import numpy as np
import matplotlib.pyplot as plt
from numpy.linalg import solve,lstsq

## read argument as the testcase
testcase = sys.argv[1]

## filename = Read in netlist file, filter out EOL
## ori_N = Number of bias points (nominal)
if testcase == "1":
    filename = "netlist_1"
    ori_N = 7
elif testcase == "2":
    filename = "netlist_2a"
    ori_N = 4
    ##ori_N = 3
elif testcase == "3":
    filename = "netlist_2b"
    ori_N = 3
else:
    filename = "netlist_1"
    ori_N = 7

content = [line.rstrip() for line in open(filename)]

N = ori_N

## Reorder the order for composition purpose, R -> V -> I -> F -> G
V = []
R = []
I = []
F = []
G = []
for i in content:
    if i:
        a = list(filter(lambda x: x != "",i.split(" ")[1:]))
        if i[0] == "V":
            V.append(a)
        if i[0] == "R":
            R.append(a)
        if i[0] == "I":
            I.append(a)
        if i[0] == "F":
            F.append(a)
        if i[0] == "G":
            G.append(a)

netlist_matrix = R+V+I+F+G

actual_N = ori_N+len(V)+len(F) ## Actual number of points. According to the damping algorithm, we take voltage/current source as additional bias points.
impedance_matrix = np.zeros((actual_N,actual_N),float) ## Form the inital matrix of impedance.
current_matrix = np.zeros((actual_N,1))
## print(netlist_matrix)
## print(impedance_matrix)

## First put all points connecting with resistance
for j in range(len(R)):
    x = int(R[j][0])-1
    y = int(R[j][1])-1
    value = float(1/float(R[j][2]))
    if not (x == -1 or y == -1):
        impedance_matrix[x][x] += value
        impedance_matrix[y][y] += value
        impedance_matrix[x][y] -= value
        impedance_matrix[y][x] -= value
    else:
        x = max(x,y)
        impedance_matrix[x][x] += value

## Next add additional rows/columns information for voltage source
#print(impedance_matrix)
for j in range(len(V)):
    x = int(V[j][0])-1
    y = int(V[j][1])-1
    if x != -1:
        impedance_matrix[N+j][x] += 1.0
        impedance_matrix[x][N+j] += 1.0
        current_matrix[N+j] = float(V[j][2]) 
    if y != -1:
        impedance_matrix[N+j][y] -= 1.0
        impedance_matrix[y][N+j] -= 1.0
        current_matrix[N+j] = float(V[j][2])

## update N since we need new N for F element
N = N+len(V)

## Stamping for independent current source
for j in range(len(I)):
    x = int(I[j][0])-1
    y = int(I[j][1])-1
    if x != -1:
        current_matrix[x] -= float(I[j][2]) 
    if y != -1:
        current_matrix[y] += float(I[j][2]) 

## Stamping for F-elements(Voltage dependent current source)
"""
## Self-defined solution
for j in range(len(F)):
    x = int(F[j][0])-1
    y = int(F[j][1])-1
    s = int(F[j][2])-1
    t = int(F[j][3])-1
    resist = 1.0
    for i in R:
        if i[0:2] == [str(s+1),str(t+1)] or i[0:2] == [str(s+1),str(t+1)]:
            resist = float(i[2])
    if x != -1:
        impedance_matrix[x][N+j] += float(F[j][4])
    if y != -1:
        impedance_matrix[y][N+j] -= float(F[j][4])
    if s != -1:
        impedance_matrix[N+j][s] = 1.0/resist
        impedance_matrix[N+j][N+j] = -1.0
    if t != -1:
        impedance_matrix[N+j][t] = -1.0/resist
        impedance_matrix[N+j][N+j] = -1.0

"""
for j in range(len(F)):
    x = int(F[j][0])-1
    y = int(F[j][1])-1
    s = int(F[j][2])-1
    t = int(F[j][3])-1
    if x != -1:
        impedance_matrix[x][N+j] += float(int(F[j][4]))
    if y != -1:
        impedance_matrix[y][N+j] -= float(int(F[j][4]))
    if s != -1:
        impedance_matrix[N+j][s] += 1.0
        impedance_matrix[s][N+j] += 1.0
    if t != -1:
        impedance_matrix[N+j][t] -= 1.0
        impedance_matrix[t][N+j] -= 1.0

## update N in case that we are extending this Python file in the future for more available element in netlist
N = N+len(F)

## Stamping for G-elements(Voltage controlled current source)
for j in range(len(G)):
    x = int(G[j][0])-1
    y = int(G[j][1])-1
    s = int(G[j][2])-1
    t = int(G[j][3])-1
    value = float(G[j][4])
    if not (x == -1 or s == -1):
        impedance_matrix[x][s] += value
    if not (x == -1 or t == -1):
        impedance_matrix[x][t] -= value
    if not (y == -1 or s == -1):
        impedance_matrix[y][s] -= value
    if not (y == -1 or t == -1):
        impedance_matrix[y][t] += value

## ---------------------------------------------- All Stamping Finished ----------------------------------------------  

## debug print out
print(impedance_matrix)
print(current_matrix)

## solve the result
result = solve(impedance_matrix,current_matrix)

N = ori_N
## print result
for i in range(len(result)):
    if i < N:
        print("Bias voltage at point",i+1,"equals",result[i][0],"volts")
    else:
        print(result[i][0])

