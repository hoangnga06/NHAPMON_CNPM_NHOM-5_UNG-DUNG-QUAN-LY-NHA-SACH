import json
import os
import unicodedata
import re 

def normalize_text(text):
    if not text:
        return "khac"

    # chuẩn hoá unicode
    text = unicodedata.normalize('NFD', text)

    # bỏ dấu tiếng Việt
    text = ''.join(ch for ch in text if unicodedata.category(ch) != 'Mn')

    # bỏ ký tự đặc biệt, khoảng trắng thừa
    text = re.sub(r'\s+', ' ', text).strip()

    return text.lower()

BOOK_FILE = "books.json"

# ==========================
# LOAD / SAVE
# ==========================
def load_books():
    if not os.path.exists(BOOK_FILE):
        return {}
    with open(BOOK_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_books(books):
    with open(BOOK_FILE, "w", encoding="utf-8") as f:
        json.dump(books, f, indent=4, ensure_ascii=False)

def generate_next_book_id(books):
    if not books:
        return "a000"

    max_num = -1
    for bid in books.keys():
        if bid.startswith("a") and bid[1:].isdigit():
            num = int(bid[1:])
            if num > max_num:
                max_num = num

    return f"a{max_num + 1:03d}"


# ======================
# NHẬP KHO (NHAPHANG GỌI)
# ======================
def import_books(items):
    books = load_books()

    for i in items:
        bid = i["book_id"]
        if bid in books:
            books[bid]["qty"] += i["qty"]
            books[bid]["price"] = i["price"]
        else:
            books[bid] = {
                "name": i["name"],
                "author": i["author"],
                "category": i["category"],
                "price": i["price"],
                "qty": i["qty"]
            }

    save_books(books)


# ============================================
# CHỈNH SỬA THÔNG TIN SÁCH (ADMIN)
# (KHÔNG SỬA SỐ LƯỢNG)
# ============================================
def edit_book():
    books = load_books()
    if not books:
        print("❌ Chưa có sách nào.")
        return

    print("\n=== CHỈNH SỬA SÁCH ===")
    book_id = input("Mã sách: ").strip()

    if book_id not in books:
        print("❌ Không tồn tại sách!")
        return

    b = books[book_id]

    name = input(f"Tên ({b['name']}): ") or b["name"]
    author = input(f"Tác giả ({b['author']}): ") or b["author"]
    category = input(f"Thể loại ({b['category']}): ") or b["category"]

    try:
        price_input = input(f"Giá ({b['price']}): ")
        price = float(price_input) if price_input else b["price"]
        if price <= 0:
            print("❌ Giá phải > 0")
            return
    except:
        print("❌ Giá không hợp lệ")
        return

    books[book_id].update({
        "name": name,
        "author": author,
        "category": category,
        "price": price
    })

    save_books(books)
    print("✅ Cập nhật thành công (SL giữ nguyên)")


# ============================================
# XÓA SÁCH
# ============================================
def delete_book():
    books = load_books()
    if not books:
        print("❌ Kho sách trống.")
        return

    print("\n=== XÓA SÁCH ===")
    book_id = input("Nhập mã sách: ").strip()

    if book_id not in books:
        print("❌ Không tìm thấy sách!")
        return

    if input("Xác nhận xóa? (y/n): ").lower() == "y":
        del books[book_id]
        save_books(books)
        print("✅ Đã xóa sách.")
    else:
        print("❌ Hủy thao tác.")


# ============================================
# XEM DANH SÁCH SÁCH
# ============================================
def view_books(show_pause=True):
    books = load_books()

    if not books:
        print("❌ Không có dữ liệu.")
        return

    # =============================
    # GOM SÁCH THEO THỂ LOẠI
    # =============================
    categories = {}

    for book_id, b in books.items():
       raw_cat = b.get("category", "Khác")
       norm_cat = normalize_text(raw_cat)

       if norm_cat not in categories:
         categories[norm_cat] = {
            "display": raw_cat,   # giữ để hiển thị
            "items": []
         }

       categories[norm_cat]["items"].append((book_id, b))

    # =============================
    # HIỂN THỊ THEO TỪNG KHUNG
    # =============================
    for data in categories.values():
       cat_name = data["display"]
       items = data["items"]

       print("\n" + "=" * 100)
       print(f"📚 THỂ LOẠI: {cat_name.upper()}")
       print("=" * 100)

       print("{:<10} {:<25} {:<20} {:<10} {:<10}".format(
         "Mã", "Tên sách", "Tác giả", "Giá", "SL"))
       print("-" * 100)

       for book_id, b in items:
         print("{:<10} {:<25} {:<20} {:<10} {:<10}".format(
            book_id,
            b["name"],
            b["author"],
            b["price"],
            b["qty"]
         ))

# ============================================
# TÌM KIẾM SÁCH
# ============================================
def search_book():
    books = load_books()

    if not books:
        print("❌ Không có sách để tìm.")
        return

    print("\n=== 🔍 TÌM KIẾM SÁCH ===")
    print("Có thể tìm theo: mã sách / tên sách / tác giả / thể loại")
    keyword = input("Nhập từ khóa: ").strip().lower()

    results = {}

    for book_id, b in books.items():
        if (
            keyword in book_id.lower()
            or keyword in b["name"].lower()
            or keyword in b["author"].lower()
            or keyword in b["category"].lower()
        ):
            results[book_id] = b

    if not results:
        print("❌ Không tìm thấy sách phù hợp.")
        return

    print("\n=== 📘 KẾT QUẢ TÌM KIẾM ===")
    print("{:<10} {:<25} {:<20} {:<15} {:<10} {:<10}".format(
        "Mã", "Tên sách", "Tác giả", "Thể loại", "Giá", "SL"
    ))
    print("-" * 95)

    for book_id, b in results.items():
        print("{:<10} {:<25} {:<20} {:<15} {:<10} {:<10}".format(
            book_id,
            b["name"],
            b["author"],
            b["category"],
            b["price"],
            b["qty"]
        ))

    input("\nNhấn Enter để quay lại menu...")

# ============================================
# MENU
# ============================================
def main(role):
    while True:
        print("\n==== QUẢN LÝ SÁCH ====")
        if role == "admin":
            print("1. Chỉnh sửa sách")
            print("2. Xóa sách")
            print("3. Xem danh sách")
            print("4. Tìm kiếm")
            print("0. Quay lại")
            c = input("Chọn: ")

            if c == "1":
                edit_book()
            elif c == "2":
                delete_book()
            elif c == "3":
                view_books()
            elif c == "4":
                search_book()
            elif c == "0":
                break
            else:
                print("❌ Sai lựa chọn")
        else:
            print("1. Xem danh sách")
            print("2. Tìm kiếm")
            print("0. Quay lại")
            c = input("Chọn: ")

            if c == "1":
                view_books()
            elif c == "2":
                search_book()
            elif c == "0":
                break
            else:
                print("❌ Lựa chọn không hợp lệ")
