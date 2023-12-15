import json
B = dict([
    ("+",.001),
    ("-",.999)
])
E = dict([
    ("+",.002),
    ("-",.998)
])
A_BE = dict([
    ("+++",.95),
    ("++-",.05),
    ("+-+",.94),
    ("+--",.06),
    ("-++",.29),
    ("-+-",.71),
    ("--+",.001),
    ("---",.999),    
])
A_J = dict([
    ("++",.9),
    ("+-",.1),
    ("-+",.05),
    ("--",.95)
])
pm = ["+","-"]
p = "+"
JA_BE = {}
for j in pm:
    for a in pm:
        for b in pm:
            for e in pm:
                JA_BE[j+a+b+e]=A_J[a+j]*A_BE[a+b+e]

J_BE = {}
for j in pm:
    for b in pm:
        for e in pm:
            J_BE[j+b+e]= JA_BE[j+"+"+b+e]+JA_BE[j+"-"+b+e]

EJ_B = {}
for e in pm:
    for j in pm:
        for b in pm:
            EJ_B[e+j+b]= E[e]*J_BE[j+b+e]

J_B = {}
for j in pm:
    for b in pm:
        J_B[j+b]=EJ_B["+"+j+b]+EJ_B["-"+j+b]

JB = {}
for j in pm:
    for b in pm:
        JB[j+b]=B[b]*J_B[j+b]

J = {}
for j in pm:
    J[j]=JB[j+"+"]+JB[j+"-"]

B_J = {}
for b in pm:
    for j in pm:
        B_J[b+j]=JB[j+b]/J[j]

print(print(json.dumps(B_J, indent = 4)))