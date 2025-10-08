with open("UCLN.Inp") as f:
    m,n = map(int,f.readline().split())

def ucln(a,b):
    while a != b:
        if a>b: a= a-b
        else: b= b-a
    return a

with open("UCLN.Out","w") as f:
    f.write(str(ucln(m,n)))