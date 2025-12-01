# Danh sách khách hàng (tái sử dụng từ người 1)
ds_khachhang = [
    {"ten": "Nguyen Van A", "sdt": "0901234567", "email": "avan@gmail.com"},
    {"ten": "Tran Thi B",    "sdt": "0912345678", "email": "btran@gmail.com"},
    {"ten": "Le Van C",      "sdt": "0987654321", "email": "cvan@gmail.com"},
    {"ten": "Pham Hong D",   "sdt": "0933334444", "email": "dpham@gmail.com"},
]
# Hàm tìm kiếm khách hàng (Không sửa danh sách gốc)
def tim_kiem_khach_hang(keyword):
    # Copy danh sách gốc → không làm thay đổi dữ liệu ban đầu
    ket_qua = []
    # Chuyển keyword về chữ thường để tìm kiếm tối ưu
    key = keyword.lower()
    for kh in ds_khachhang:
        # So khớp keyword với Tên / Sdt / Email
        if (key in kh["ten"].lower() or
            key in kh["sdt"].lower() or
            key in kh["email"].lower()):
            ket_qua.append(kh.copy())   # copy để không sửa bản gốc

    return ket_qua

# Giả lập UI tìm kiếm (Menu)
def giao_dien_tim_kiem():
    print("Tìm kiếm khách hàng")
    keyword = input("Nhập từ khóa (tên/ số điện thoại/ email): ")
    ket_qua = tim_kiem_khach_hang(keyword)
    print(f"\n Đã tìm thấy {len(ket_qua)} kết quả!\n")

    # Hiển thị kết quả – (được phép vì không sửa danh sách gốc)
    for kh in ket_qua:
        print(f"Tên: {kh['ten']}")
        print(f"Sdt: {kh['sdt']}")
        print(f"Email: {kh['email']}")