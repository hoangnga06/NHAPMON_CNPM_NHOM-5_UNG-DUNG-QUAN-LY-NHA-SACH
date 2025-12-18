import json
import os

BOOK_FILE = "books.json"

def load_books():
    if not os.path.exists(BOOK_FILE):
        return {}
    with open(BOOK_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_books():
    with open(BOOK_FILE, "w", encoding="utf-8") as f:
        json.dump(books, f, indent=4, ensure_ascii=False)

# =============================
# QUẢN LÝ SÁCH - FULL CODE
# =============================

# Database giả lập
books = load_books()

# ============================================
# 1) THÊM SÁCH MỚI — add_new_book()
# ============================================
def add_new_book():
    pass

# ============================================
# 2) CHỈNH SỬA TT SÁCH — edit_book()
# ============================================
def edit_book():
    pass

# ============================================
# 3) XÓA SÁCH — delete_book()
# ============================================
def delete_book():
    pass

# ============================================
# 4) XEM DANH SÁCH SÁCH — view_books()
# ============================================
def view_books(show_pause=True):
    pass


# ============================================
# 5) TÌM KIẾM SÁCH — search_book()
# ============================================
def search_book():
    pass

# ============================================
# MENU CHÍNH — main()
# ============================================
def main(role):
    while True:
        print("\n==== QUẢN LÝ SÁCH ====")
        if role == "admin":
            print("1. Thêm sách mới")
            print("2. Chỉnh sửa thông tin sách")
            print("3. Xóa sách")
            print("4. Xem danh sách sách")
            print("5. Tìm kiếm sách")
            print("6. Thoát")
            choice = input("Chọn: ")
            if choice == "1":
                add_new_book()
            elif choice == "2":
                edit_book()
            elif choice == "3":
                delete_book()
            elif choice == "4":
                view_books()
            elif choice == "5":
                search_book()
            elif choice == "6":
                break
            else:
                print("❌ Lựa chọn không hợp lệ!")
        else:  # USER
            print("1. Xem danh sách sách")
            print("2. Tìm kiếm sách")
            print("3. Thoát")
            choice = input("Chọn: ")
            if choice == "1":
                view_books()
            elif choice == "2":
                search_book()
            elif choice == "3":
                break
            else:
                print("❌ Lựa chọn không hợp lệ!")