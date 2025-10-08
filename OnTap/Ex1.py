with open("tong.inp","w") as f:
    nhap_n = input("Nhap so n :")
    f.write(nhap_n)

with open("tong.inp") as f2:
    n = int(f2.read())



tong = 0
for i in  range(1,n+1):
    tong+= 1/(i**2)

s=str(round(tong,3))

with open("tong.out","w") as a:
    a.write(s)