import json
import os
from datetime import datetime
import KHACHHANG

BOOK_FILE = "books.json"
SALE_FILE = "sales.json"

# ======================
# LOAD / SAVE
# ======================
def load_books():
    if not os.path.exists(BOOK_FILE):
        return {}
    with open(BOOK_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_books(books):
    with open(BOOK_FILE, "w", encoding="utf-8") as f:
        json.dump(books, f, indent=4, ensure_ascii=False)

def load_sales():
    if not os.path.exists(SALE_FILE):
        return []
    with open(SALE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_sales(sales):
    with open(SALE_FILE, "w", encoding="utf-8") as f:
        json.dump(sales, f, indent=4, ensure_ascii=False)

# ======================
# GIỎ HÀNG
# ======================
def add_to_cart(cart):
    pass
# XEM GIỎ HÀNG
def view_cart(cart):
    pass
# ======================
# IN HÓA ĐƠN
# ======================
def print_invoice(inv):
    pass
# ======================
# THANH TOÁN
# ======================
def checkout(cart, staff_email):
    pass

# ======================
# MENU BÁN HÀNG (USER)
# ======================
def sales_menu(staff_email):
    cart = {}   # ❗ GIỎ HÀNG SỐNG TRONG SUỐT PHIÊN

    while True:
        print("\n===== BÁN HÀNG =====")
        print("1. Thêm sách vào giỏ")
        print("2. Xem giỏ hàng")
        print("3. Sửa giỏ hàng")
        print("4. Thanh toán")
        print("0. Quay lại")

        ch = input("Chọn: ")

        if ch == "1":
            add_to_cart(cart)
        elif ch == "2":
            view_cart(cart)
        elif ch == "3":
            update_cart(cart)
        elif ch == "4":
            checkout(cart, staff_email)
        elif ch == "0":
            break
        else:
            print("❌ Lựa chọn không hợp lệ")
