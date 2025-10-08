with open("Kangaroo.Inp") as  f:
    n,a,b = map(int, f.readline().split())

for y in range(n//b,-1,-1):
    if(n-b*y) % a == 0:
        solan_nhaymin = y+ ((n-b*y) // a)
        break
print(solan_nhaymin)

with open("Kangaroo.Out","w") as f:
    f.write(str(solan_nhaymin))