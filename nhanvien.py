# ==============================
#  DATABASE GIẢ LẬP
# ==============================

employees = [
    {"id": 1, "name": "Nguyễn A", "email": "a@gmail.com", "phone": "0901", "role": "admin"},
    {"id": 2, "name": "Nguyễn B", "email": "b@gmail.com", "phone": "0902", "role": "staff"},
]


# ==============================
# THÊM NHÂN VIÊN
# ==============================
def add_employee(name, email, phone, role):
    # Kiểm tra trùng SĐT
    for emp in employees:
        if emp["phone"] == phone:
            return "❌ Số điện thoại đã tồn tại!"

    new_id = employees[-1]["id"] + 1 if employees else 1
    new_emp = {"id": new_id, "name": name, "email": email, "phone": phone, "role": role}
    employees.append(new_emp)

    return "✔ Thêm nhân viên thành công!"


# ==============================
# CHỈNH SỬA NHÂN VIÊN
# ==============================
def update_employee(emp_id, name=None, email=None, phone=None, role=None):
    pass

# ==============================
# XOÁ NHÂN VIÊN
# ==============================
def delete_employee(emp_id):
    pass
# ==============================
# XEM DANH SÁCH NHÂN VIÊN + TÌM KIẾM
# ==============================
def view_employees(search=""):
    pass


# ==============================
# MAIN CHẠY CHƯƠNG TRÌNH
# ==============================
def main():
    print("=== QUẢN LÝ NHÂN VIÊN ===")

    while True:
        print("\n1. Xem ds")
        print("2. Thêm nhân viên")
        print("3. Chỉnh sửa nhân viên")
        print("4. Xoá nhân viên")
        print("0. Thoát")

        choice = input("Chọn chức năng: ")

        # ---------------- XEM DANH SÁCH
        if choice == "1":
            keyword = input("Nhập từ khoá tìm kiếm (Enter để bỏ qua): ")
            print(view_employees(keyword))

        # ---------------- THÊM
        elif choice == "2":
            name = input("Tên: ")
            email = input("Email: ")
            phone = input("SĐT: ")
            role = input("Vai trò: ")
            print(add_employee(name, email, phone, role))

        # ---------------- SỬA
        elif choice == "3":
            emp_id = int(input("Nhập ID nhân viên cần sửa: "))
            name = input("Tên mới (Enter bỏ qua): ")
            email = input("Email mới: ")
            phone = input("SĐT mới: ")
            role = input("Vai trò mới: ")
            print(update_employee(emp_id, name, email, phone, role))

        # ---------------- XOÁ
        elif choice == "4":
            emp_id = int(input("ID cần xoá: "))
            print(delete_employee(emp_id))

        # ---------------- THOÁT
        elif choice == "0":
            print("Đã thoát chương trình.")
            break

        else:
            print("Lựa chọn không hợp lệ!")


# chạy chương trình
main()
