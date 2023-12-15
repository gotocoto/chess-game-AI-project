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
A_M = dict([
    ("++",.7),
    ("+-",.3),
    ("-+",.01),
    ("--",.99)
])
pm = ["+","-"]
p = ["+"]

BEAJM = {}
for b in pm:
    for e in pm:
        for a in pm:
            for j in pm:
                for m in pm:
                    BEAJM[b+e+a+j+m]= B[b]*E[e]*A_BE[a+b+e]*A_J[a+j]*A_M[a+m]
print(sum(BEAJM.values()))
newJB = {}
for j in pm:
    for b in pm:
        sum = 0
        for e in pm:
            for a in pm:
                for m in pm:
                    sum+=BEAJM[b+e+a+j+m]
        newJB[j+b]=sum
newJ = {}
for j in pm:
        sum = 0
        for b in pm:
            for e in pm:
                for a in pm:
                    for m in pm:
                        sum+=BEAJM[b+e+a+j+m]
        newJ[j]=sum
JA_BE = {}
for j in p:
    for a in pm:
        for b in pm:
            for e in pm:
                JA_BE[j+a+b+e]=A_J[a+j]*A_BE[a+b+e]

J_BE = {}
for j in p:
    for b in pm:
        for e in pm:
            J_BE[j+b+e]= JA_BE[j+"+"+b+e]+JA_BE[j+"-"+b+e]

EJ_B = {}
for e in pm:
    for j in p:
        for b in pm:
            EJ_B[e+j+b]= E[e]*J_BE[j+b+e]

J_B = {}
for j in p:
    for b in pm:
        J_B[j+b]=EJ_B["+"+j+b]+EJ_B["-"+j+b]

JB = {}
for j in p:
    for b in pm:
        JB[j+b]=B[b]*J_B[j+b]

J = {}
for j in p:
    J[j]=JB[j+"+"]+JB[j+"-"]

B_J = {}
for b in pm:
    for j in p:
        B_J[b+j]=JB[j+b]/J[j]
print("P(Burglary|John Calls = +j):\n")
print(print(json.dumps(B_J, indent = 4)))

#print(print(json.dumps(JB, indent = 4)))
#print(print(json.dumps(newJB, indent = 4)))

#print(print(json.dumps(J, indent = 4)))
#print(print(json.dumps(newJ, indent = 4)))