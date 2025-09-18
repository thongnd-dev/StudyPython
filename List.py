from random import randrange

n =int(input("Nhap vao so phan tu: "))
ls = [0]*n

for i in range(n):
    ls[i] = randrange(1,101)
