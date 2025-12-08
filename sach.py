# =============================
#   QUẢN LÝ SÁCH - FULL CODE
# =============================

# Database giả lập
books = {}

# ============================================
# 1) THÊM SÁCH MỚI  — add_new_book()
# ============================================
def add_new_book():
    """
    Chức năng:
    - Thiết kế form nhập thông tin
    - API thêm sách (giả lập)
    - Kiểm tra trùng mã
    - Lưu vào hệ thống
    """
    print("\n=== THÊM SÁCH MỚI ===")

    book_id = input("Nhập mã sách: ")
    if book_id in books:
        print("❌ Mã sách đã tồn tại!")
        return

    name = input("Tên sách: ")
    author = input("Tác giả: ")
    category = input("Thể loại: ")

    try:
        price = float(input("Giá: "))
        qty = int(input("Số lượng: "))
    except:
        print("Giá hoặc số lượng không hợp lệ!")
        return

    if price <= 0 or qty < 0:
        print("Giá phải > 0 và số lượng ≥ 0!")
        return

    # Lưu vào database
    books[book_id] = {
        "name": name,
        "author": author,
        "category": category,
        "price": price,
        "qty": qty
    }

    print("Thêm sách thành công!")

# ============================================
# 2) CHỈNH SỬA THÔNGT SÁCH — edit_book()
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
def main():
    while True:
        print("\n====== QUẢN LÝ SÁCH ======")
        print("1. Thêm sách mới")
        print("2. Chỉnh sửa thông tin sách")
        print("3. Xóa sách")
        print("4. Xem danh sách sách")
        print("5. Tìm kiếm sách")
        print("6. Thoát")

        choice = input("Chọn chức năng: ")

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
            print("👋 Thoát chương trình.")
            break
        else:
            print("❌ Lựa chọn không hợp lệ!")


if __name__ == "__main__":
    main()