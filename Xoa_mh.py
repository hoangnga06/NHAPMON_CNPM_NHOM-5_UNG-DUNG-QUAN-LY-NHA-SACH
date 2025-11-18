# Danh sách sách (giả lập database)
books = [
    {"id": 1, "title": "Doraemon tập 1"},
    {"id": 2, "title": "Python cơ bản"},
    {"id": 3, "title": "Bút bi"}
]


def delete_book(book_id):
    # Xác nhận xóa
    confirm = input("Bạn có chắc muốn xóa sách này? (y/n): ")
    if confirm.lower() != "y":
        print(" Đã hủy thao tác xóa.")
        return

    # Tìm sách trong ds
    for book in books:
        if book["id"] == book_id:
            books.remove(book)

            # Giả lập gửi request DELETE
            print(f"➡ Gửi request: DELETE /books/{book_id}")

            print(" Xóa thành công!")
            print(" Danh sách sau khi xóa:", books)
            return

    print("Không tìm thấy sách để xóa!")
