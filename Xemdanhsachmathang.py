#XEM DANH SÁCH MẶT HÀNG
danh_sach_mat_hang = [
    {"ma_hang": "MH001", "ten": "Sách Toán", "gia": 25000},
    {"ma_hang": "MH002", "ten": "Sách Văn", "gia": 30000},
    {"ma_hang": "MH003", "ten": "Sách Anh", "gia": 28000},
    {"ma_hang": "MH004", "ten": "Bút bi", "gia": 5000},
    {"ma_hang": "MH005", "ten": "Vở kẻ ngang", "gia": 12000},
    {"ma_hang": "MH006", "ten": "Máy tính Casio", "gia": 450000},
    {"ma_hang": "MH007", "ten": "Thước kẻ", "gia": 7000},
]

# Số dòng mỗi trang
so_dong = 3

def xem_danh_sach_trang(trang):
    print(f"\n--- DANH SÁCH MẶT HÀNG - TRANG {trang} ---")

    bat_dau = (trang - 1) * so_dong
    ket_thuc = bat_dau + so_dong

    # Lấy dữ liệu theo trang
    ds_trang = danh_sach_mat_hang[bat_dau:ket_thuc]

    # Nếu trang không có dữ liệu → báo lỗi
    if not ds_trang:
        print("Không có dữ liệu ở trang này!")
        return

    # Hiển thị bảng
    for mh in ds_trang:
        print(f"{mh['ma_hang']:6} | {mh['ten']:20} | Giá: {mh['gia']}đ")

# CHẠY CHƯƠNG TRÌNH
trang = 1
while True:
    xem_danh_sach_trang(trang)

    # Điều hướng phân trang
    lua_chon = input("\nNhập (n) trang tiếp, (p) trang trước, (q) thoát: ")
    if lua_chon == "n":
        trang += 1
    elif lua_chon == "p" and trang > 1:
        trang -= 1
    elif lua_chon == "q":
        break
    else:
        print("Lựa chọn không hợp lệ!")