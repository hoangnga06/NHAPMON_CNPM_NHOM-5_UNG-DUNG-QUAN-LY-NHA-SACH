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

    # tìm nhân viên
    for emp in employees:
        if emp["id"] == emp_id:

            # validate đơn giản
            if phone:
                for e in employees:
                    if e["phone"] == phone and e["id"] != emp_id:
                        return "❌ Số điện thoại đã tồn tại!"

            # cập nhật thông tin
            if name: emp["name"] = name
            if email: emp["email"] = email
            if phone: emp["phone"] = phone
            if role: emp["role"] = role

            return "✔ Cập nhật thành công!"

    return "❌ Không tìm thấy nhân viên!"

# ==============================
# XOÁ NHÂN VIÊN
# ==============================
def delete_employee(emp_id):
    for emp in employees:
        if emp["id"] == emp_id:

            if emp["role"] == "admin":
                return "Không được xoá admin chính!"

            employees.remove(emp)
            return "✔ Đã xoá nhân viên!"

    return "Không tìm thấy nhân viên!"
# ==============================
# XEM DANH SÁCH NHÂN VIÊN + TÌM KIẾM
# ==============================
def view_employees(search=""):
    result = []
    search = search.lower()

    for emp in employees:
        if (search in emp["name"].lower()) or (search in emp["email"].lower()) or (search in emp["phone"]):
            result.append(emp)

    if not result:
        return "❗ Không có dữ liệu nhân viên!"

    return result

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
