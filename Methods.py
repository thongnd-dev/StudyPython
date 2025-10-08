


class sinhvien():
    def __init__(self, hoten:str, ma_sinh_vien:int, que_quan:str, tongdiem:float =0):
        self.hoten = hoten
        self.ma_sinh_vien = ma_sinh_vien
        self.que_quan = que_quan
        self.tongdiem = tongdiem
        assert tongdiem>=0
sv1 = sinhvien("nguyen van a",2,"abd",3)
sv2 = sinhvien("nguyen van b", 3,"fds", 4)

print(sv1.hoten + " co tong diem la: " + str(sv1.tongdiem))
