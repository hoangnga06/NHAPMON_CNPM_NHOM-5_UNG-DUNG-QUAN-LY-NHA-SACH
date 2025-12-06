# ===========================
# DỮ LIỆU NGƯỜI DÙNG TRONG HỆ THỐNG
# ===========================
users = []  ## Mỗi user: {"email": ..., "password": ..., "role": ..., "locked": False, "login_fail": 0}
session = {"logged_in": False, "email": None}  ## Giả lập phiên đăng nhập


# ===========================
# 1) ĐĂNG KÝ TÀI KHOẢN (FORM + API)
# ===========================
def register_user():
    pass
# ===========================
# 2) ĐĂNG NHẬP HT
# ===========================
def login_user():
    pass


# ===========================
# 3) ĐĂNG XUẤT (THAY THẾ CHO ĐỔI MẬT KHẨU)
# ===========================
def logout_user():
    pass

# ===========================
# 4) GÁN QUYỀN NGƯỜI DÙNG + XEM DANH SÁCH
# ===========================
def manage_roles():
    pass
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
