# =============================
#   QUẢN LÝ SÁCH - FULL CODE
# =============================

# Database giả lập
books = {}

# ============================================
# 1) THÊM SÁCH MỚI  — add_new_book()
# ============================================
def add_new_book():
    pass

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