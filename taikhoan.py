import json
import os
import re
import hashlib
import sach
import khachhang


DATA_FILE = "users.json"

# ======================
# LOAD / LƯU
# ======================
def load_users():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_users(users):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4, ensure_ascii=False)

def hash_password(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

def valid_email(email):
    return re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email)

def valid_password(pw):
    return len(pw) >= 6

users = load_users()
session = {"logged_in": False, "email": None}

# ======================
# TẠO ADMIN BAN ĐẦU
# ======================
def create_default_admin():
    for u in users:
        if u["role"] == "admin":
            return
    users.append({
        "fullname": "Administrator",
        "email": "admin@gmail.com",
        "password": hash_password("admin123"),
        "role": "admin",
        "locked": False,
        "login_fail": 0
    })
    save_users(users)

create_default_admin()

# ======================
# ĐĂNG KÝ
# ======================
def valid_phone(phone):
    pass

def register():
    pass
# ======================
# ĐĂNG NHẬP
# ======================
def login():
    pass

# ======================
# ĐỔI MẬT KHẨU
# ======================
def change_password():
    pass

# ======================
# ADMIN QLND
# ======================
def admin_menu():
    pass

# ======================
# MENU
# ======================
def main():
    while True:

        # =========================
        # CHƯA ĐĂNG NHẬP
        # =========================
        if not session["logged_in"]:
            print("\n=== HỆ THỐNG QUẢN LÝ NHÀ SÁCH ===")
            print("1. Đăng ký")
            print("2. Đăng nhập")
            print("3. Thoát")

            ch = input("Chọn: ")

            if ch == "1":
                register()
            elif ch == "2":
                login()
            elif ch == "3":
                print("Thoát chương trình.")
                break
            else:
                print("❌ Lựa chọn sai.")

        # =========================
        # ĐÃ ĐĂNG NHẬP
        # =========================
        else:
            user = next(u for u in users if u["email"] == session["email"])
            while True:
                print(f"\n=== MENU ({user['role'].upper()}) ===")
                print("1. Quản lý sách")
                print("2. Quản lý khách hàng")
                print("3. Đổi mật khẩu")

                if user["role"] == "admin":
                   print("4. Quản lý (Admin)")
                   print("5. Đăng xuất")
                else:
                   print("4. Đăng xuất")

                ch = input("Chọn: ")

                # =========================
                # SÁCH
                # =========================
                if ch == "1":
                   sach.main(user["role"])      # 👈 admin / user tự phân quyền bên sach.py

                # =========================
                # KHÁCH HÀNG
                # =========================
                elif ch == "2":
                   khachhang.main()             # 👈 admin & user đều dùng được

                # =========================
                # ĐỔI MẬT KHẨU
                # =========================
                elif ch == "3":
                   change_password()

                # =========================
                # ADMIN
                # =========================
                elif ch == "4" and user["role"] == "admin":
                   admin_menu()

                # =========================
                # ĐĂNG XUẤT
                # =========================
                elif (ch == "4" and user["role"] == "user") or \
             (ch == "5" and user["role"] == "admin"):

                   session["logged_in"] = False
                   session["email"] = None
                   print("✔ Đã đăng xuất.")
                   break

                else:
                   print("❌ Lựa chọn sai.")
            
           


if __name__ == "__main__":
    main()
