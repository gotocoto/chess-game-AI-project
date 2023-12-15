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

JA_BE = {}
for con in ["++","+-","-+","--"]:
    for act in ["++","+-","-+","--"]:
        JA_BE[act+con]=A_J[act]*A_BE[act[0]+con]

J_BE = {}
for con in ["++","+-","-+","--"]:
    for act in ["+","-"]:
        J_BE[act+con]= JA_BE[act+"+"+con]+JA_BE[act+"-"+con]

EJ_B = {}
for con in ["+","-"]:
    for act in ["++","+-","-+","--"]:
        EJ_B[act+con]= E[act[0]]*J_BE[act[0]+con+act[0]]

J_B = {}
for con in ["+","-"]:
    for act in ["+","-"]:
        J_B[act+con]=EJ_B[act+"+"+con]+EJ_B[act+"-"+con]

JB = {}
for act in ["++","+-","-+","--"]:
    JB[act]=B[act[1]]*J_B[act]

J = {}
for act in ["+","-"]:
    J[act]=JB[act+"+"]+JB[act+"-"]

B_J = {}
for con in ["+","-"]:
    for act in ["+","-"]:
        B_J[act+con]=JB[con+act]/J[con]

print(print(json.dumps(B_J, indent = 4)))