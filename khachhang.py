import sqlite3

# ==========================
#   KẾT NỐI + TẠO BẢNG
# ==========================
def connect_db():
    return sqlite3.connect("bookstore.db")

def create_table():
    pass


# ==========================
#     THÊM KH
# ==========================
def add_customer():
    pass

# ==========================
#    CHỈNH SỬA KHÁCH HÀNG
# ==========================
def edit_customer():
    pass
# ==========================
#   XEM DANH SÁCH KHÁCH HÀNG
# ==========================
def view_customers():
    pass
# ==========================
#     TÌM KIẾM KHÁCH
# ==========================
def search_customer():
    pass

# ==========================
#           MAIN
# ==========================
def main():
    create_table()
    while True:
        print("\n===== MENU KHÁCH HÀNG =====")
        print("1. Thêm khách hàng")
        print("2. Chỉnh sửa khách hàng")
        print("3. Xem danh sách khách")
        print("4. Tìm kiếm khách hàng")
        print("0. Thoát")

        ch = input("Chọn chức năng: ")

        if ch == "1": add_customer()
        elif ch == "2": edit_customer()
        elif ch == "3": view_customers()
        elif ch == "4": search_customer()
        elif ch == "0":
            print("Bye 👋")
            break
        else:
            print(" Lựa chọn không hợp lệ!")


if __name__ == "__main__":
    main()
