import sqlite3

# ==========================
#   KẾT NỐI + TẠO BẢNG
# ==========================
def connect_db():
    return sqlite3.connect("bookstore.db")

def create_table():
    conn = connect_db()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS customers(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT UNIQUE NOT NULL,
            address TEXT
        )
    """)
    conn.commit()
    conn.close()


# ==========================
#     THÊM KH
# ==========================
def add_customer():
    print("\n=== THÊM KHÁCH HÀNG ===")
    name = input("Tên: ").strip()
    phone = input("SĐT: ").strip()
    address = input("Địa chỉ: ").strip()

    if not name or not phone:
        print("⚠ Không được để trống tên hoặc SĐT")
        return

    conn = connect_db()
    c = conn.cursor()

    # kiểm tra trùng SĐT
    c.execute("SELECT * FROM customers WHERE phone=?", (phone,))
    if c.fetchone():
        print("⚠ SĐT đã tồn tại!")
        conn.close()
        return

    c.execute("INSERT INTO customers(name, phone, address) VALUES (?, ?, ?)",
              (name, phone, address))
    conn.commit()
    conn.close()
    print("✔ Thêm khách hàng thành công!")

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
