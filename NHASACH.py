import TAIKHOAN
import SACH
import KHACHHANG
import NHANVIEN
import BANHANG
import NHAPHANG
import BAOCAO



def main():
    TAIKHOAN.create_default_admin()

    while True:
        # =========================
        # CHƯA ĐĂNG NHẬP
        # =========================
        if not TAIKHOAN.session["logged_in"]:
            print("\n=== HỆ THỐNG QUẢN LÝ NHÀ SÁCH ===")
            print("1. Đăng ký")
            print("2. Đăng nhập")
            print("3. Thoát")

            ch = input("Chọn: ")

            if ch == "1":
                TAIKHOAN.register()
            elif ch == "2":
                TAIKHOAN.login()
            elif ch == "3":
                print("👋 Thoát chương trình.")
                break
            else:
                print("❌ Lựa chọn sai.")

        # =========================
        # ĐÃ ĐĂNG NHẬP
        # =========================
        else:
            users = TAIKHOAN.load_users()
            user = next((u for u in users if u["email"] == TAIKHOAN.session["email"]), None)

            if not user:
                TAIKHOAN.session["logged_in"] = False
                TAIKHOAN.session["email"] = None
                break

            while True:
                print(f"\n=== MENU ({user['role'].upper()}) ===")

                if user["role"] == "user":
                    print("1. Quản lý sách")
                    print("2. Bán hàng")
                    print("3. Quản lý khách hàng")
                    print("4. Đổi mật khẩu")
                    print("5. Đăng xuất")

                    ch = input("Chọn: ")
                    if ch == "1":
                        SACH.main("user")
                    elif ch == "2":
                        BANHANG.sales_menu(user["email"])
                    elif ch == "3":
                        KHACHHANG.main("user")
                    elif ch == "4":
                        TAIKHOAN.change_password()
                    elif ch == "5":
                        TAIKHOAN.session["logged_in"] = False
                        TAIKHOAN.session["email"] = None
                        break
                    

                else:  # ADMIN
                    print("1. Quản lý sách")
                    print("2. Quản lý khách hàng")
                    print("3. Quản lý nhân viên")
                    print("4. Quản lý tài khoản")
                    print("5. Nhập hàng")
                    print("6. Báo cáo")
                    print("7. Đổi mật khẩu")
                    print("8. Đăng xuất")
                   

                    ch = input("Chọn: ")
                    if ch == "1":
                        SACH.main("admin")
                    elif ch == "2":
                        KHACHHANG.main("admin")
                    elif ch == "3":
                        NHANVIEN.main()
                    elif ch == "4":
                        TAIKHOAN.admin_menu(user["email"])
                    elif ch == "5":
                        NHAPHANG.nhaphang_menu(user["email"])
                    elif ch == "6":
                        BAOCAO.menu_baocao()
                    elif ch == "7":
                        TAIKHOAN.change_password()
                    elif ch == "8":
                        TAIKHOAN.session["logged_in"] = False
                        TAIKHOAN.session["email"] = None
                        break


if __name__ == "__main__":
    main()
