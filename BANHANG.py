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

def next_invoice_id(sales):
    if not sales:
        return 1
    return max(s["id"] for s in sales) + 1


# ======================
# GIỎ HÀNG
# ======================
def add_to_cart(cart):
    books = load_books()
    keyword = input("Nhập tên sách: ").lower()

    matches = [(bid, b) for bid, b in books.items()
               if keyword in b["name"].lower()]

    if not matches:
        print("❌ Không tìm thấy sách")
        return

    print("\n--- KẾT QUẢ TÌM KIẾM ---")
    for i, (bid, b) in enumerate(matches, 1):
        print(f"{i}. {b['name']} | Giá: {b['price']} | Tồn: {b['qty']}")

    try:
        idx = int(input("Chọn sách: ")) - 1
        book_id, book = matches[idx]
    except:
        print("❌ Lựa chọn không hợp lệ")
        return

    try:
        qty = int(input("Số lượng: "))
    except:
        print("❌ Số lượng không hợp lệ")
        return

    if qty <= 0:
        print("❌ Số lượng phải > 0")
        return

    if qty > book["qty"]:
        print("❌ Không đủ tồn kho")
        return

    if book_id in cart:
        if cart[book_id]["qty"] + qty > book["qty"]:
            print("❌ Tổng số lượng vượt tồn kho")
            return
        cart[book_id]["qty"] += qty
    else:
        cart[book_id] = {
            "book_id": book_id,
            "name": book["name"],
            "price": book["price"],
            "qty": qty
        }

    print("✅ Đã thêm vào giỏ hàng")


def view_cart(cart):
    if not cart:
        print("🛒 Giỏ hàng trống")
        return

    print("\n=== GIỎ HÀNG ===")
    total = 0
    for i, item in enumerate(cart.values(), 1):
        amount = item["price"] * item["qty"]
        total += amount
        print(f"{i}. {item['name']} x{item['qty']} = {amount:,.0f}")

    print(f"Tổng tiền: {total:,.0f}")


def update_cart(cart):
    if not cart:
        print("🛒 Giỏ hàng trống")
        return

    books = load_books()
    view_cart(cart)
    keys = list(cart.keys())

    try:
        idx = int(input("Chọn sách cần sửa: ")) - 1
        bid = keys[idx]
    except:
        print("❌ Lựa chọn không hợp lệ")
        return

    print("1. Thay đổi số lượng")
    print("2. Xóa khỏi giỏ")
    ch = input("Chọn: ")

    if ch == "1":
        try:
            new_qty = int(input("Số lượng mới: "))
        except:
            print("❌ Không hợp lệ")
            return

        if new_qty <= 0:
            del cart[bid]
            print("✅ Đã xóa sách khỏi giỏ")
        elif new_qty > books[bid]["qty"]:
            print("❌ Vượt quá tồn kho")
        else:
            cart[bid]["qty"] = new_qty
            print("✅ Đã cập nhật số lượng")

    elif ch == "2":
        del cart[bid]
        print("✅ Đã xóa sách khỏi giỏ")


# ======================
# IN HÓA ĐƠN
# ======================
def print_invoice(inv):
    print("\n" + "=" * 60)
    print("               HÓA ĐƠN NHÀ SÁCH")
    print("=" * 60)
    print(f"Mã đơn     : {inv['id']}")
    print(f"Thời gian  : {inv['time']}")
    print(f"Nhân viên  : {inv['staff']}")
    print("-" * 60)
    print(f"Khách hàng : {inv['customer']['name']}")
    print(f"SĐT        : {inv['customer']['phone']}")
    print(f"Địa chỉ    : {inv['customer']['address']}")
    print("-" * 60)

    print("{:<25}{:>5}{:>12}{:>12}".format("Sách", "SL", "Giá", "TT"))
    for i in inv["items"]:
        print("{:<25}{:>5}{:>12,.0f}{:>12,.0f}".format(
            i["name"][:25], i["qty"], i["price"], i["price"] * i["qty"]
        ))

    print("-" * 60)
    print(f"Tổng tiền : {inv['total']:>35,.0f}")
    print(f"Giảm giá  : {inv['discount']:>35,.0f}")
    print(f"Khách trả : {inv['pay']:>35,.0f}")
    print("=" * 60)
    print("         CẢM ƠN QUÝ KHÁCH ❤️")


# ======================
# THANH TOÁN
# ======================
def checkout(cart, staff_email):
    if not cart:
        print("❌ Giỏ hàng trống")
        return

    phone = input("SĐT khách: ").strip()
    if not KHACHHANG.valid_phone(phone):
        print("❌ SĐT không hợp lệ")
        return

    customer = KHACHHANG.get_or_create_customer("", phone, "")
    if not customer:
        print("📌 Khách mới")
        name = input("Tên: ").strip()
        address = input("Địa chỉ: ").strip()
        customer = KHACHHANG.get_or_create_customer(name, phone, address)
        if not customer:
            print("❌ Không thể tạo khách")
            return

    books = load_books()
    for bid, item in cart.items():
        if books[bid]["qty"] < item["qty"]:
            print(f"❌ Không đủ tồn kho: {item['name']}")
            return

    total = sum(i["price"] * i["qty"] for i in cart.values())

    print("1. Giảm theo %")
    print("2. Giảm theo tiền")
    opt = input("Chọn: ")
    discount = 0

    if opt == "1":
        percent = float(input("Nhập %: "))
        discount = total * percent / 100
    elif opt == "2":
        discount = float(input("Nhập tiền giảm: "))
    else:
        print("❌ Lựa chọn sai")
        return

    pay = total - discount
    if input("Xác nhận thanh toán (y/n): ").lower() != "y":
        return

    for bid, item in cart.items():
        books[bid]["qty"] -= item["qty"]
    save_books(books)

    sales = load_sales()
    invoice = {
        "id": next_invoice_id(sales),
        "time": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "staff": staff_email,
        "customer": customer,
        "items": list(cart.values()),
        "total": total,
        "discount": discount,
        "pay": pay
    }

    sales.append(invoice)
    save_sales(sales)

    print_invoice(invoice)
    cart.clear()


# ======================
# MENU BÁN HÀNG
# ======================
def sales_menu(staff_email):
    cart = {}
    while True:
        print("\n===== BÁN HÀNG =====")
        print("1. Thêm sách vào giỏ")
        print("2. Xem giỏ")
        print("3. Sửa giỏ")
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
