with open("SOTHUMANG.INP") as f:
    a= f.readlines()

list_out = []
for element in a[1].split():
    tong = 0

    for number in element:
        tong += int(number)**3
    if(tong == int(element)):
        list_out.append(element)
list_out.sort()

chuoi_out =""
for x in list_out:
    chuoi_out+=str(x)+" "

with open("SOTHUMANG.OUT","w") as wri:
    wri.write(chuoi_out)