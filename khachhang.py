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


customers = load_customers()


# ==========================
# THÊM KHÁCH
# ==========================
def add_customer():
    pass

# ==========================
# SỬA KHÁCH
# ==========================
def edit_customer():
    pass


# ==========================
# XEM DS KHÁCH
# ==========================
def view_customers():
    pass

# ==========================
# TÌM KIẾM
# ==========================
def search_customer():
    pass

# ==========================
# MENU KHÁCH HÀNG
# ==========================
def main():
    while True:
        print("\n===== MENU KHÁCH HÀNG =====")
        print("1. Thêm khách hàng")
        print("2. Chỉnh sửa khách hàng")
        print("3. Xem danh sách khách")
        print("4. Tìm kiếm khách hàng")
        print("0. Quay lại")

        ch = input("Chọn: ")

        if ch == "1":
            add_customer()
        elif ch == "2":
            edit_customer()
        elif ch == "3":
            view_customers()
        elif ch == "4":
            search_customer()
        elif ch == "0":
            break
        else:
            print("❌ Lựa chọn không hợp lệ!")