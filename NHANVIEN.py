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
    pass
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
