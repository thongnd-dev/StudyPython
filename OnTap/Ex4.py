ls =["banana","apple", "mango","watermelon", "coconut"]

ls_new =[]
for i in ls:
    if "a" in i:
        ls_new.append(i)
print(ls_new)

ls_new2 = [i.upper() for i in ls if "a" in i]
print(ls_new2)

ls2 = [1,3,5,9,8,4]

ls_new3 = [i**2 for i in ls2 if i**2 %2 == 0]
print(ls_new3)