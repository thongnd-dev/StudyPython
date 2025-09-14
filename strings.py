a = "english = 78 science = 83 math = 68 History = 65"
tach = a.split()
print(tach)

s = 0
for i in tach:
    if i.isdigit():
        s+=int(i)

print(s)