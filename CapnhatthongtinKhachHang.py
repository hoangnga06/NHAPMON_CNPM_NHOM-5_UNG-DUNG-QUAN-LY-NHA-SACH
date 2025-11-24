# CẬP NHẬT THÔNG TIN KHÁCH HÀNG
import re
import requests

# Hàm kiểm tra định dạng email
def kiem_tra_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

# Hàm cập nhật thông tin khách hàng
def cap_nhat_khach_hang():
    print("=== CẬP NHẬT THÔNG TIN KHÁCH HÀNG ===")

    id_kh = input("Nhập ID khách hàng cần cập nhật: ")

    ten = input("Tên mới: ").strip()
    sdt = input("Số điện thoại: ").strip()
    email = input("Email: ").strip()
    dia_chi = input("Địa chỉ: ").strip()

    # --- VALIDATION ---
    if ten == "":
        print("❌ Tên không được để trống!")
        return

    if not kiem_tra_email(email):
        print("❌ Email không đúng định dạng!")
        return

    if not sdt.isdigit():
        print("❌ Số điện thoại phải là số!")
        return
    
    # --- Dữ liệu gửi lên API ---
    du_lieu = {
        "name": ten,
        "phone": sdt,
        "email": email,
        "address": dia_chi
    }

    # --- Gửi API PUT /customers/{id} ---
    url = f"http://example.com/api/customers/{id_kh}"
    # (Trong thực tế cần bật API, đây chỉ minh họa)
    # response = requests.put(url, json=du_lieu)
    # return response.json()

    # Demo: Giả lập gọi API thành công
    return f"Cập nhật khách hàng {id_kh} thành công!"