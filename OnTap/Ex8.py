with open("DayXN.Inp") as f:
    m,n = map(int, f.readline().split())
"""
def total(s:str):
    t = 0
    for i in s:
        t += int(i)**2
    return t
ls = []
ls.append(m)
temp = m
for i in range(1,n):
    ls.append(total(str(temp)))
    temp = int(total(str(temp)))

str_out = ""
for st in ls:
    str_out += str(st) + " "
with open("DayXN.Out","w") as f:
    f.write(str_out)
"""
def f(x):
    return sum([int(i)**2 for i in str(x)])

with open("DayXN.Out","w") as fi:
    for i in range(n):
        fi.write((str(m)) + " ")
        m = f(m)