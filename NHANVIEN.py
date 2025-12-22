import json
import os

DATA_FILE = "users.json"

# ======================
# LOAD / SAVE
# ======================
def load_users():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_users(users):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4, ensure_ascii=False)

# ======================
# CẬP NHẬT THÔNG TIN NHÂN VIÊN
# (hiện dữ liệu cũ, sửa chỗ cần)
# ======================
def update_info():
    users = load_users()
    email = input("Email nhân viên: ").strip()

    for u in users:
        if u["email"] == email:
            print("\n--- Thông tin hiện tại ---")
            print(f"Giới tính   : {u.get('gender','')}")
            print(f"Địa chỉ     : {u.get('address','')}")
            print(f"Ngày vào làm: {u.get('start_date','')}")

            print("\n--- Nhập thông tin mới (Enter để giữ nguyên) ---")
            u["gender"] = input(f"Giới tính [{u.get('gender','')}]: ") or u.get("gender","")
            u["address"] = input(f"Địa chỉ [{u.get('address','')}]: ") or u.get("address","")
            u["start_date"] = input(f"Ngày vào làm [{u.get('start_date','')}]: ") or u.get("start_date","")

            save_users(users)
            print("✔ Đã cập nhật thông tin nhân viên.")
            return

    print("❌ Không tìm thấy nhân viên.")

# ======================
# XOÁ NHÂN VIÊN (XOÁ USER)
# ======================
def delete_user():
    pass

# ======================
# TÌM KIẾM NHÂN VIÊN
# ======================
def search_user():
    pass
# ======================
# XEM DANH SÁCH NHÂN VIÊN
# ======================
def view_users():
    pass
# ======================
# MENU
# ======================
def main():
    while True:
        print("\n=== QUẢN LÝ NHÂN VIÊN ===")
        print("1. Cập nhật thông tin nhân viên")
        print("2. Xoá nhân viên")
        print("3. Tìm kiếm nhân viên")
        print("4. Xem danh sách nhân viên")
        print("5. Quay lại")

        ch = input("Chọn: ")

        if ch == "1":
            update_info()
        elif ch == "2":
            delete_user()
        elif ch == "3":
            search_user()
        elif ch == "4":
            view_users()
        elif ch == "5":
            break
        else:
            print("❌ Lựa chọn sai.")
