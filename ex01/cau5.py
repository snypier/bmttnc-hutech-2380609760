so_gio_lam = float(input("Nhap so gio lam: "))
luong_gio = float(input("Nhập thù lao trên mỗi giờ làm tiêu chuẩn"))
gio_tiêun_chuan =44
gio_vuot_chuan = max(0, so_gio_lam - gio_tiêun_chuan)
thuc_linh = (gio_tiêun_chuan * luong_gio) + (gio_vuot_chuan * luong_gio * 1.5)

print(f"tiền thực lĩnh của nhân viên là: {thuc_linh}")