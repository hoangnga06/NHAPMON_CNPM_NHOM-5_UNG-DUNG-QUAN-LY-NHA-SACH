# Danh sách khách hàng mẫu
khach_hang = [
    {"MaKH": "KH01", "Ten": "Nguyen Van A", "SDT": "0901234567"},
    {"MaKH": "KH02", "Ten": "Tran Thi B", "SDT": "0987654321"},
    {"MaKH": "KH03", "Ten": "Le Van C",     "SDT": "0911122233"}
]

def hien_danh_sach():
    print("\n--- DANH SÁCH KHÁCH HÀNG ---")
    for kh in khach_hang:
        print(f"MãKH: {kh['MaKH']} - Tên: {kh['Ten']} - SĐT: {kh['SDT']}")
    print("--------------------------------")


def xoa_khach_hang():
    hien_danh_sach()

    key = input("\nNhập MãKH hoặc SĐT cần xóa: ").strip()

    # Tìm khách hàng theo MãKH hoặc SĐT
    kh_can_xoa = None
    for kh in khach_hang:
        if kh["MaKH"] == key or kh["SDT"] == key:
            kh_can_xoa = kh
            break

    if kh_can_xoa is None:
        print("❌ Không tìm thấy khách hàng.")
        return

    # Hộp thoại xác nhận
    xac_nhan = input(f"Bạn có chắc muốn xóa khách hàng '{kh_can_xoa['Ten']}'? (y/n): ")

    if xac_nhan.lower() == "y":
        khach_hang.remove(kh_can_xoa)
        print("✅ Đã xóa thành công!")
    else:
        print("❌ Hủy thao tác xóa.")

    # Reload danh sách
    hien_danh_sach()


# Chạy chương trình
xoa_khach_hang()
