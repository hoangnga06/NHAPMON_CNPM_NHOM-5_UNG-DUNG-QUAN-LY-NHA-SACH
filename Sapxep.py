#sapxep
# Danh sách sách mẫu
sach_list = [
    {"ten": "Dế Mèn Phiêu Lưu Ký", "gia": 45000, "so_luong": 12, "ngay_nhap": "2024-03-18"},
    {"ten": "Tuổi Thơ Dữ Dội", "gia": 55000, "so_luong": 5, "ngay_nhap": "2024-04-02"},
    {"ten": "Lão Hạc", "gia": 30000, "so_luong": 20, "ngay_nhap": "2024-02-15"},
    {"ten": "Tắt Đèn", "gia": 38000, "so_luong": 8,   "ngay_nhap": "2024-03-25"},
]

# --- Các chức năng sắp xếp ---

def sap_xep_hang_moi_ve(ds):
    """Sắp xếp theo hàng mới về (ngày nhập mới nhất trước)."""
    return sorted(ds, key=lambda x: x["ngay_nhap"], reverse=True)

def sap_xep_so_luong(ds):
    """Sắp xếp theo sl tồn (từ cao đến thấp)."""
    return sorted(ds, key=lambda x: x["so_luong"], reverse=True)

def sap_xep_ten(ds):
    """Sx theo tên từ A → Z."""
    return sorted(ds, key=lambda x: x["ten"].lower())

def sap_xep_gia(ds):
    """Sắp xếp theo giá từ thấp → cao."""
    return sorted(ds, key=lambda x: x["gia"])
