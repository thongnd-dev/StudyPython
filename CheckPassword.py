n = input("Vui long nhap mat khau: ")

x = bool
y = bool
count = 1
for i in n:
    if i.isdigit():
        x=True
        break
    else:
        x = False
for i in n:
    if i.isalpha():
        y=True
        break
    else:
        y = False
while len(n) <6 or x==False or y == False:
        n= input("Nhap lai mat khau, it nhat 6 ky tu, 1 chu cai, 1 so:")
        for i in n:
            if i.isdigit():
                x = True
                break
            else:
                x = False
        for i in n:
            if i.isalpha():
                y = True
                break
            else:
                y = False
else:
    print("Mat khau hop le:")

logins = input("Nhap mat khau he thong: ")
while logins != n:
    count=count+1
    logins = input(f"Nhap sai mat khau, nhap sai {count}/5 lan: ")
    if count == 5:
        print("Ban nhap sai mat khau qua 5 lan, khoa dang nhap")
        break
else:
    print("Dang nhap thanh cong")
