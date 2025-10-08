with open("XepHang.INP") as f:
    n = int(f.readline())
    ls = list(map(int, f.readline().split()))

ls_dem = []
for i in range(n):
    t = ls.count(ls[i])
    ls_dem.append(t)

solan = max(ls_dem)
chieucao = ls[ls_dem.index((solan))]

chuoi_out = str(solan) + " " + str(chieucao)

with open("XepHang.OUT","w") as f:
    f.write(chuoi_out)