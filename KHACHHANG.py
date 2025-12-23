import json
import os

CUSTOMER_FILE = "customers.json"

# ==========================
# LOAD / SAVE
# ==========================
def load_customers():
    if not os.path.exists(CUSTOMER_FILE):
        return {}
    with open(CUSTOMER_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_customers(customers):
    with open(CUSTOMER_FILE, "w", encoding="utf-8") as f:
        json.dump(customers, f, indent=4, ensure_ascii=False)

def valid_phone(phone):
    return (
        phone.isdigit()
        and phone.startswith("0")
        and len(phone) == 10
    )

customers = load_customers()


# ==========================
# LẤY HOẶC TẠO KHÁCH (DÙNG CHO BÁN HÀNG)
# ==========================
def get_or_create_customer(name, phone, address):
    global customers
    phone = phone.strip()
    # kiểm tra SĐT hợp lệ
    if not valid_phone(phone):
        return None

    # tìm theo SĐT (khách cũ)
    for cid, c in customers.items():
        if c["phone"] == phone:
            return {
                "id": cid,
                "name": c["name"],
                "phone": c["phone"],
                "address": c["address"]
            }

    # chưa có → tạo mới(chỉ khi đủ thông tin)
    if not name or not address:
        return None
    cid = str(len(customers) + 1)
    customers[cid] = {
        "name": name,
        "phone": phone,
        "address": address
    }
    save_customers(customers)

    return {
        "id": cid,
        "name": name,
        "phone": phone,
        "address": address
    }



# ==========================
# SỬA KHÁCH
# ==========================
def edit_customer():
    global customers
    print("\n=== CHỈNH SỬA KHÁCH ===")

    cid = input("Nhập ID khách: ").strip()

    if cid not in customers:
        print(" Không tìm thấy khách!")
        return

    c = customers[cid]

    print(f"Tên hiện tại: {c['name']}")
    print(f"SĐT hiện tại: {c['phone']}")
    print(f"Địa chỉ hiện tại: {c['address']}")

    new_name = input("Tên mới (Enter bỏ qua): ") or c["name"]
    new_phone = input("SĐT mới (Enter bỏ qua): ").strip()
    new_address = input("Địa chỉ mới (Enter bỏ qua): ") or c["address"]
    if new_phone:
        if not valid_phone(new_phone):
            print("❌ SĐT phải bắt đầu bằng 0 và đủ 10 số")
            return
    else:
        new_phone = c["phone"]

    # kiểm tra trùng SĐT
    for k, v in customers.items():
        if k != cid and v["phone"] == new_phone:
            print(" SĐT đã được dùng bởi khách khác!")
            return

    customers[cid] = {
        "name": new_name,
        "phone": new_phone,
        "address": new_address
    }

    save_customers(customers)
    print("✅ Cập nhật thành công!")


# ==========================
# XEM Danh Sach KHÁCH
# ==========================
def view_customers():
    
    print("\n=== DANH SÁCH KHÁCH HÀNG ===")

    if not customers:
        print(" Chưa có khách hàng.")
        return

    print("{:<5} {:<20} {:<15} {:<30}".format("ID", "Tên", "SĐT", "Địa chỉ"))
    print("-" * 70)

    for cid, c in customers.items():
        print("{:<5} {:<20} {:<15} {:<30}".format(
            cid, c["name"], c["phone"], c["address"]
        ))
# ==========================
# TÌM KIẾM
# ==========================
def search_customer():
    print("\n=== TÌM KIẾM KHÁCH ===")
    key = input("Nhập tên hoặc SĐT: ").lower()

    found = False
    for cid, c in customers.items():
        if key in c["name"].lower() or key in c["phone"]:
            if not found:
                print("{:<5} {:<20} {:<15} {:<30}".format("ID", "Tên", "SĐT", "Địa chỉ"))
                print("-" * 70)
            found = True
            print("{:<5} {:<20} {:<15} {:<30}".format(
                cid, c["name"], c["phone"], c["address"]
            ))

    if not found:
        print("❌ Không tìm thấy khách phù hợp.")
    
# ==========================
# MENU KHÁCH HÀNG
# ==========================
def main(role):
    while True:
        print("\n===== MENU KHÁCH HÀNG =====")
        print("1. Chỉnh sửa khách hàng")
        print("2. Xem danh sách khách")
        print("3. Tìm kiếm khách hàng")
        print("0. Quay lại")

        ch = input("Chọn: ")
        if ch == "1":
            edit_customer()
        elif ch == "2":
            view_customers()
        elif ch == "3":
            search_customer()
        elif ch == "0":
            break
        else:
            print("❌ Lựa chọn không hợp lệ!")
