import json
import os
import re
import hashlib
import SACH
import KHACHHANG
import NHANVIEN 

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

session = {"logged_in": False, "email": None}

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
    return (
        phone.isdigit()
        and phone.startswith("0")
        and len(phone) == 10
    )

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
    # Kiểm tra trùng SĐT
    if any(u.get("phone") == phone for u in users):
        print("❌ SĐT đã được đăng ký.")
        return

    if not valid_password(pw):
        print("❌ Mật khẩu ≥ 6 ký tự.")
        return
    if pw != cf:
        print("❌ Mật khẩu xác nhận không khớp.")
        return
    # Kiểm tra trùng email
    if any(u["email"] == email for u in users):
        print("❌ Email đã tồn tại.")
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
    email = input("Email: ")
    pw = input("Mật khẩu: ")

    for u in users:
        if u["email"] == email:
            if u["locked"]:
                print("Tài khoản bị khóa.")
                return
            if u["password"] == hash_password(pw):
                session["logged_in"] = True
                session["email"] = email
                u["login_fail"] = 0
                save_users(users)
                print("✔ Đăng nhập thành công.")
                return
            else:
                u["login_fail"] += 1
                print(f"Sai mật khẩu ({u['login_fail']}/3)")
                if u["login_fail"] >= 3:
                    u["locked"] = True
                    print("⚠ Tài khoản đã bị khóa.")
                save_users(users)
                return
    print("Email không tồn tại.")

# ======================
# ĐỔI MẬT KHẨU
# ======================
def change_password():
    if not session["logged_in"]:
        print("❌ Chưa đăng nhập.")
        return

    old = input("Mật khẩu cũ: ")
    new = input("Mật khẩu mới: ")
    cf = input("Xác nhận mật khẩu mới: ")
    users = load_users()

    for u in users:
        if u["email"] == session["email"]:
            # Kiểm tra mật khẩu cũ
            if u["password"] != hash_password(old):
                print("❌ Mật khẩu cũ sai.")
                return
            # Kiểm tra mật khẩu mới khác mật khẩu cũ
            if hash_password(new) == u["password"]:
                print("❌ Mật khẩu mới không được trùng mật khẩu cũ.")
                return
            # Kiểm tra độ mạnh
            if not valid_password(new):
                print("❌ Mật khẩu ≥ 6 ký tự.")
                return
            # Xác nhận
            if new != cf:
                print("❌ Xác nhận không khớp.")
                return
            # Lưu mật khẩu mới
            u["password"] = hash_password(new)
            save_users(users)
            print("✔ Đổi mật khẩu thành công.")
            return


# ======================
# ADMIN QLND
# ======================
def admin_menu():
    while True:
        users = load_users()
        print("\n=== ADMIN ===")
        print("1. Xem users")
        print("2. Đổi quyền")
        print("3. Khóa/Mở")
        print("4. Quay lại")

        c = input("Chọn: ")

        if c == "1":
            for u in users:
                print(f"{u['email']} |  {u.get('phone', '---')}| {u['role']} | locked={u['locked']}")
        elif c == "2":
            email = input("Email: ")
            role = input("Role (admin/user): ")
            found = False
            for u in users:
                if u["email"] == email:
                    u["role"] = role
                    save_users(users)
                    print("✔ Đã đổi quyền.")
                    found  = True
                    break
            if not found:
                print("❌ Tài khoản không tồn tại")

        elif c == "3":
            email = input("Email: ")
            found = False
            for u in users:
                if u["email"] == email:
                    u["locked"] = not u["locked"]
                    save_users(users)
                    print("✔ Đã cập nhật.")
                    found = True
                    break
            if not found:
                print("❌ Không tìm thấy tài khoản")
        elif c == "4":
            break



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
            users = load_users()
            user = next((u for u in users if u["email"] == session["email"]), None)
            if not user:
               print("❌ Tài khoản không tồn tại.")
               session["logged_in"] = False
               break
           
            while True:
                print(f"\n=== MENU ({user['role'].upper()}) ===")
                if user["role"] == "user":
                    print("1. Quản lý sách")
                    print("2. Bán hàng")
                    print("3. Quản lý khách hàng")
                    print("4. Đổi mật khẩu")
                    print("5. Đăng xuất")

                else:  # admin
                    print("1. Quản lý sách")
                    print("2. Quản lý khách hàng")
                    print("3. Quản lý nhân viên")
                    print("4. Quản lý tài khoản")
                    print("5. Đổi mật khẩu")
                    print("6. Đăng xuất")

                ch = input("Chọn: ")
                # USER
                if user["role"] == "user":
                    if ch == "1":
                       SACH.main("user")
                    elif ch == "2":
                       import BANHANG
                       BANHANG.sales_menu(user["email"])
                    elif ch == "3":
                       KHACHHANG.main("user")
                    elif ch == "4":
                       change_password()
                    elif ch == "5":
                        session["logged_in"] = False
                        session["email"] = None
                        print("✔ Đã đăng xuất.")
                        break

                # ADMIN
                else:
                    if ch == "1":
                        SACH.main("admin")
                    elif ch == "2":
                        KHACHHANG.main("admin")
                    elif ch == "3":
                        NHANVIEN.main()
                    elif ch == "4":
                        admin_menu()
                    elif ch == "5":
                        change_password()
                    elif ch == "6":
                        session["logged_in"] = False
                        session["email"] = None
                        print("✔ Đã đăng xuất.")
                        break               

if __name__ == "__main__":
    main()