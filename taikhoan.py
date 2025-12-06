# ===========================
# DỮ LIỆU NGƯỜI DÙNG TRONG HỆ THỐNG
# ===========================
users = []  ## Mỗi user: {"email": ..., "password": ..., "role": ..., "locked": False, "login_fail": 0}
session = {"logged_in": False, "email": None}  ## Giả lập phiên đăng nhập


# ===========================
# 1) ĐĂNG KÝ TÀI KHOẢN (FORM + API)
# ===========================
def register_user():

    print("\n=== FORM ĐĂNG KÝ TÀI KHOẢN ===")
    email = input("Nhập email: ")
    password = input("Nhập mật khẩu: ")

    ## ---- API ĐĂNG KÝ GIẢ LẬP ----
    new_user = {
        "email": email,
        "password": password,
        "role": "user",
        "locked": False,
        "login_fail": 0
    }

    users.append(new_user)  ## Lưu vào database (tạm)
    print("✔ API /auth/register → Đăng ký thành công.")
    

# ===========================
# 2) ĐĂNG NHẬP HT
# ===========================
def login_user():
    print("\n=== MÀN HÌNH ĐĂNG NHẬP ===")
    print("(Email, Mật khẩu, Nút 'Đăng nhập')")

    email = input("Email: ")
    password = input("Mật khẩu: ")

    ## Tìm user trong database
    for u in users:
        if u["email"] == email:

            # Nếu tài khoản đang khóa
            if u["locked"]:
                print("❌ Tài khoản đã bị khóa do nhập sai quá nhiều.")
                return

            # Kiểm tra đúng mật khẩu
            if u["password"] == password:
                session["logged_in"] = True
                session["email"] = email

                u["login_fail"] = 0  # reset số lần sai

                print("✔ Đăng nhập thành công!")
                print("API /auth/login → 200 OK")
                print(f"➡ Quyền của bạn: {u['role']}")

                # Lưu log đăng nhập
                print(f"[LOG] {email} đã đăng nhập vào hệ thống.")
                return

            # Sai mật khẩu => tăng số lần sai
            else:
                u["login_fail"] += 1
                print("❌ Sai mật khẩu.")

                # Sai 3 lần → khóa
                if u["login_fail"] >= 3:
                    u["locked"] = True
                    print("⚠ Tài khoản đã bị khóa sau 3 lần đăng nhập sai.")
                return

    print("❌ Không tìm thấy tài khoản.")


# ===========================
# 3) ĐĂNG XUẤT (THAY THẾ CHO ĐỔI MẬT KHẨU)
# ===========================
def logout_user():
    print("\n=== ĐĂNG XUẤT HỆ THỐNG ===")

    if not session["logged_in"]:
        print("❌ Bạn chưa đăng nhập.")
        return

    print("✔ Nhấn nút 'Đăng xuất' → Xử lý...")

    session["logged_in"] = False
    session["email"] = None

    print("✔ Phiên đăng nhập đã được hủy.")
    print("➡ Chuyển về trang Đăng nhập.")

    # Kiểm tra quyền sau đăng xuất
    print("⚠ Nếu truy cập chức năng yêu cầu đăng nhập → sẽ bị chặn.")

# ===========================
# 4) GÁN QUYỀN NGƯỜI DÙNG + XEM DANH SÁCH
# ===========================
def manage_roles():
    print("\n=== QUẢN LÝ QUYỀN NGƯỜI DÙNG ===")

    print("\n--- DANH SÁCH NGƯỜI DÙNG ---")
    for u in users:
        print(f"{u['email']} - Quyền: {u['role']} - Khóa: {u['locked']}")
    if not users:
        print("Chưa có người dùng.")

    print("\n--- GÁN QUYỀN ---")
    email = input("Nhập email người muốn đổi quyền: ")
    role = input("Quyền mới (admin / user): ")

    for u in users:
        if u["email"] == email:
            u["role"] = role
            print("✔ Gán quyền thành công.")
            return

    print("❌ Không tìm thấy người dùng.")
# ===========================
# MENU CHÍNH
# ===========================
def main():
    while True:
        print("\n=== QUẢN LÝ NGƯỜI DÙNG ===")
        print("1. Đăng ký tài khoản")
        print("2. Đăng nhập")
        print("3. Đăng xuất")
        print("4. Quản lý quyền người dùng")
        print("5. Thoát")

        choice = input("Chọn chức năng: ")

        if choice == "1":
            register_user()
        elif choice == "2":
            login_user()
        elif choice == "3":
            logout_user()
        elif choice == "4":
            manage_roles()
        elif choice == "5":
            print("Kết thúc chương trình.")
            break
        else:
            print("❌ Lựa chọn không hợp lệ.")


if __name__ == "__main__":
    main()
