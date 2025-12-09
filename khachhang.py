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
    print("\n=== CHỈNH SỬA KHÁCH ===")
    cid = input("Nhập ID khách: ")

    if not cid.isdigit():
        print("⚠ ID không hợp lệ!")
        return

    conn = connect_db()
    c = conn.cursor()
    c.execute("SELECT * FROM customers WHERE id=?", (cid,))
    customer = c.fetchone()

    if not customer:
        print("⚠ Không tìm thấy khách")
        conn.close()
        return

    print(f"Tên hiện tại: {customer[1]}")
    print(f"SĐT hiện tại: {customer[2]}")
    print(f"Địa chỉ hiện tại: {customer[3]}")

    new_name = input("Tên mới (Enter bỏ qua): ") or customer[1]
    new_phone = input("SĐT mới: ") or customer[2]
    new_address = input("Địa chỉ mới: ") or customer[3]

    # kiểm tra trùng SĐT
    c.execute("SELECT id FROM customers WHERE phone=? AND id!=?", (new_phone, cid))
    if c.fetchone():
        print("⚠ SĐT đã được sử dụng bởi khách khác!")
        conn.close()
        return

    c.execute("""
        UPDATE customers
        SET name=?, phone=?, address=?
        WHERE id=?
    """, (new_name, new_phone, new_address, cid))

    conn.commit()
    conn.close()
    print("✔ Cập nhật khách hàng thành công!")

# ==========================
#   XEM DANH SÁCH KHÁCH HÀNG
# ==========================
def view_customers():
    print("\n=== DANH SÁCH KHÁCH ===")

    conn = connect_db()
    c = conn.cursor()
    c.execute("SELECT * FROM customers ORDER BY id DESC")
    data = c.fetchall()
    conn.close()

    if not data:
        print("⚠ Chưa có khách hàng!")
        return

    print("{:<5} {:<20} {:<15} {:<30}".format("ID", "Tên", "SĐT", "Địa chỉ"))
    print("-" * 65)
    for row in data:
        print("{:<5} {:<20} {:<15} {:<30}".format(row[0], row[1], row[2], row[3]))

# ==========================
#     TÌM KIẾM KHÁCH
# ==========================
def search_customer():
    print("\n=== TÌM KIẾM KHÁCH ===")
    key = input("Nhập tên hoặc SĐT: ")

    conn = connect_db()
    c = conn.cursor()
    c.execute("""
        SELECT * FROM customers
        WHERE name LIKE ? OR phone LIKE ?
    """, (f"%{key}%", f"%{key}%"))
    data = c.fetchall()
    conn.close()

    if not data:
        print("⚠ Không tìm thấy khách phù hợp!")
        return

    print("{:<5} {:<20} {:<15} {:<30}".format("ID", "Tên", "SĐT", "Địa chỉ"))
    print("-" * 65)
    for row in data:
        print("{:<5} {:<20} {:<15} {:<30}".format(row[0], row[1], row[2], row[3]))

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
