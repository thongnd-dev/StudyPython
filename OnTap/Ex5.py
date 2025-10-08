with open("NguyenTo.Inp") as f:
    n = int(f.readline())

tong = 0
for i in str(n):
    tong+= int(i)

check = True

for i in range(2,tong//2+1):
    if(tong % i == 0):
        check = False
        break
s_out = ""
if check:
    s_out = "YES"
else:
    s_out = "NO"

with open("NguyenTo.Out","w") as f:
    f.write(str(tong) +"\n" + s_out)

