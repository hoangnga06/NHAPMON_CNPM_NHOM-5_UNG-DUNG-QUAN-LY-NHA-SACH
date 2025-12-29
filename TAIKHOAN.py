import json
import os
import re
import hashlib

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

def hash_password(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

def valid_email(email):
    return re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email)

def valid_password(pw):
    return len(pw) >= 6

def valid_phone(phone):
    return phone.isdigit() and phone.startswith("0") and len(phone) == 10


# ======================
# SESSION
# ======================
session = {
    "logged_in": False,
    "email": None,
    "role": None
}


# ======================
# TẠO ADMIN BAN ĐẦU
# ======================
def create_default_admin():
    users = load_users()
    for u in users:
        if u["role"] == "admin":
            return

    users.append({
        "fullname": "Administrator",
        "email": "admin@gmail.com",
        "phone": "0000000000",
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
def register():
    users = load_users()
    print("\n=== ĐĂNG KÝ ===")

    fullname = input("Họ tên: ").strip()
    email = input("Email: ").strip()
    phone = input("SĐT: ").strip()
    pw = input("Mật khẩu: ")
    cf = input("Xác nhận mật khẩu: ")

    if not fullname:
        print("❌ Họ tên trống.")
        return
    if not valid_email(email):
        print("❌ Email không hợp lệ.")
        return
    if not valid_phone(phone):
        print("❌ SĐT không hợp lệ.")
        return
    if any(u["email"] == email for u in users):
        print("❌ Email đã tồn tại.")
        return
    if any(u.get("phone") == phone for u in users):
        print("❌ SĐT đã được đăng ký.")
        return
    if not valid_password(pw):
        print("❌ Mật khẩu ≥ 6 ký tự.")
        return
    if pw != cf:
        print("❌ Mật khẩu xác nhận không khớp.")
        return

    users.append({
        "fullname": fullname,
        "email": email,
        "phone": phone,
        "password": hash_password(pw),
        "role": "user",
        "locked": False,
        "login_fail": 0
    })
    save_users(users)
    print("✔ Đăng ký thành công.")


# ======================
# ĐĂNG NHẬP
# ======================
def login():
    users = load_users()
    print("\n=== ĐĂNG NHẬP ===")

    email = input("Email: ").strip()
    pw = input("Mật khẩu: ")

    for u in users:
        if u["email"] == email:
            if u["locked"]:
                print("❌ Tài khoản bị khóa.")
                return
            if u["password"] == hash_password(pw):
                session["logged_in"] = True
                session["email"] = email
                session["role"] = u["role"]
                u["login_fail"] = 0
                save_users(users)
                print("✔ Đăng nhập thành công.")
                return
            else:
                u["login_fail"] += 1
                print(f"❌ Sai mật khẩu ({u['login_fail']}/3)")
                if u["login_fail"] >= 3:
                    u["locked"] = True
                    print("⚠ Tài khoản đã bị khóa.")
                save_users(users)
                return

    print("❌ Email không tồn tại.")


# ======================
# ĐỔI MẬT KHẨU
# ======================
def change_password():
    if not session["logged_in"]:
        print("❌ Chưa đăng nhập.")
        return

    users = load_users()
    old = input("Mật khẩu cũ: ")
    new = input("Mật khẩu mới: ")
    cf = input("Xác nhận mật khẩu mới: ")

    for u in users:
        if u["email"] == session["email"]:
            if u["password"] != hash_password(old):
                print("❌ Mật khẩu cũ sai.")
                return
            if hash_password(new) == u["password"]:
                print("❌ Mật khẩu mới trùng mật khẩu cũ.")
                return
            if not valid_password(new):
                print("❌ Mật khẩu ≥ 6 ký tự.")
                return
            if new != cf:
                print("❌ Xác nhận không khớp.")
                return

            u["password"] = hash_password(new)
            save_users(users)
            print("✔ Đổi mật khẩu thành công.")
            return


# ======================
# ADMIN QUẢN LÝ USER
# ======================
def admin_menu():
    while True:
        users = load_users()
        print("\n=== ADMIN ===")
        print("1. Xem users")
        print("2. Đổi quyền")
        print("3. Khóa / Mở")
        print("0. Quay lại")

        ch = input("Chọn: ")

        if ch == "1":
            for u in users:
                print(f"{u['email']} | {u['phone']} | {u['role']} | locked={u['locked']}")

        elif ch == "2":
            email = input("Email: ").strip()
            role = input("Role (admin/user): ").strip()
            if role not in ("admin", "user"):
                print("❌ Role không hợp lệ.")
                continue

            for u in users:
                if u["email"] == email:
                    u["role"] = role
                    save_users(users)
                    print("✔ Đã đổi quyền.")
                    break
            else:
                print("❌ Không tìm thấy tài khoản.")

        elif ch == "3":
            email = input("Email: ").strip()
            for u in users:
                if u["email"] == email:
                    u["locked"] = not u["locked"]
                    save_users(users)
                    print("✔ Đã cập nhật trạng thái.")
                    break
            else:
                print("❌ Không tìm thấy tài khoản.")

        elif ch == "0":
            break
        else:
            print("❌ Lựa chọn không hợp lệ.")
