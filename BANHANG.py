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
    books = load_books()
    keyword = input("Nhập tên sách: ").lower()

    matches = []
    for bid, b in books.items():
        if keyword in b["name"].lower():
            matches.append((bid, b))

    if not matches:
        print("❌ Không tìm thấy sách")
        return

    print("\n--- KẾT QUẢ TÌM KIẾM ---")
    for i, (bid, b) in enumerate(matches, 1):
        print(f"{i}. {b['name']} | Giá: {b['price']} | Tồn: {b['qty']}")

    try:
        choice = int(input("Chọn sách: ")) - 1
        book_id, book = matches[choice]
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

    # 👉 CỘNG DỒN VÀO GIỎ
    if book_id in cart:
        cart[book_id]["qty"] += qty
    else:
        cart[book_id] = {
            "name": book["name"],
            "price": book["price"],
            "qty": qty
        }

    print("✅ Đã thêm vào giỏ hàng")
# XEM GIỎ HÀNG
def view_cart(cart):
    if not cart:
        print("🛒 Giỏ hàng trống")
        return

    print("\n=== GIỎ HÀNG ===")
    total = 0
    for i, (bid, item) in enumerate(cart.items(), 1):
        amount = item["price"] * item["qty"]
        total += amount
        print(f"{i}. {item['name']} x{item['qty']} = {amount:,.0f}")

    print(f"Tổng tiền: {total:,.0f}")
# CAP NHAT GIỎ HÀNG
def update_cart(cart):
    if not cart:
        print("🛒 Giỏ hàng trống")
        return

    view_cart(cart)
    book_ids = list(cart.keys())

    try:
        idx = int(input("Chọn sách cần sửa: ")) - 1
        book_id = book_ids[idx]
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
            del cart[book_id]
            print("✅ Đã xóa sách khỏi giỏ")
        else:
            cart[book_id]["qty"] = new_qty
            print("✅ Đã cập nhật số lượng")

    elif ch == "2":
        del cart[book_id]
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

    print("\n=== THÔNG TIN KHÁCH HÀNG ===")
    phone = input("SĐT: ").strip()
    # Kiểm tra SĐt
    if not phone:
        print("❌ Chưa nhập số điện thoại")
        return 

    if not KHACHHANG.valid_phone(phone):
        print("❌ SĐT không hợp lệ")
        return
    # thử lấy khách cũ trước
    customer = KHACHHANG.get_or_create_customer("", phone, "")
    if customer:
       print("\n📌 KHÁCH HÀNG ĐÃ TỒN TẠI")
       print(f"👤 Tên     : {customer['name']}")
       print(f"📞 SĐT     : {customer['phone']}")
       print(f"🏠 Địa chỉ : {customer['address']}")

       if input("➡️ Tiếp tục tạo hóa đơn? (y/n): ").lower() != "y":
          print("❌ Đã hủy thanh toán")
          return
    # nếu chưas có -> tạo mới
    else:
        print("📌 Khách mới, vui lòng nhập thông tin")
        name =input("👤 Tên khách:").strip()
        address=input("🏠 Địa chỉ:").strip()
        if not name or not address:
           print("❌ Không được để trống")
           return

        customer = KHACHHANG.get_or_create_customer(name, phone, address)
    # phòng trường hợp lỗi
    if not customer:
        print("❌ Không thể tạo khách hàng")
        return
        
    books = load_books()

    # kiểm tra tồn kho
    for bid, item in cart.items():
        if books[bid]["qty"] < item["qty"]:
            print(f"❌ Không đủ tồn kho: {item['name']}")
            return

    total = sum(item["price"] * item["qty"] for item in cart.values())

    print("\n=== GIẢM GIÁ ===")
    print("1. Giảm theo %")
    print("2. Giảm theo số tiền")
    opt = input("Chọn: ")

    discount = 0

    if opt == "1":
       try:
         percent = float(input("Nhập % giảm: "))
       except:
         print("❌ Dữ liệu không hợp lệ")
         return

       if percent < 0 or percent > 100:
         print("❌ % giảm phải từ 0–100")
         return

       discount = total * percent / 100

    elif opt == "2":
       try:
         discount = float(input("Nhập số tiền giảm: "))
       except:
         print("❌ Dữ liệu không hợp lệ")
         return

       if discount < 0 or discount > total:
         print("❌ Số tiền giảm không hợp lệ")
         return

    else:
       print("❌ Lựa chọn không hợp lệ")
       return

    pay = total - discount


    if input("Xác nhận thanh toán (y/n): ").lower() != "y":
        print("❌ Đã hủy thanh toán")
        return

    # 👉 TRỪ KHO DUY NHẤT Ở ĐÂY
    for bid, item in cart.items():
        books[bid]["qty"] -= item["qty"]

    save_books(books)

    sales = load_sales()
    invoice = {
        "id": len(sales) + 1,
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
