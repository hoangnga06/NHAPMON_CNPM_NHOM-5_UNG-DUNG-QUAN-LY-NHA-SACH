import json
import os
from datetime import datetime
import SACH

IMPORT_FILE = "imports.json"

# ======================
# LOAD / SAVE
# ======================
def load_imports():
    if not os.path.exists(IMPORT_FILE):
        return []
    with open(IMPORT_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_imports(data):
    with open(IMPORT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
def valid_phone(phone):
    phone = phone.strip()
    return phone.isdigit() and len(phone) == 10 and phone.startswith("0")

def search_books_by_name(books, keyword):
    keyword = keyword.lower()
    results = []
    for bid, b in books.items():
        if keyword in b["name"].lower():
            results.append((bid, b))
    return results

def choose_existing_book(matches):
    print("\n📚 SÁCH TƯƠNG TỰ ĐÃ CÓ:")
    for idx, (bid, b) in enumerate(matches, 1):
        print(f"{idx}. [{bid}] {b['name']} ({b.get('author','')})")

    choice = input("Chọn số để dùng sách cũ (Enter = thêm sách mới): ").strip()
    if not choice:
        return None

    if choice.isdigit():
        idx = int(choice)
        if 1 <= idx <= len(matches):
            return matches[idx - 1][0]

    print("❌ Lựa chọn không hợp lệ")
    return "INVALID"



# ======================
# TẠO PHIẾU + THÊM SÁCH
# ======================
def create_import(admin_email):
    imports = load_imports()
    books = SACH.load_books()
    print("\n=== TẠO PHIẾU NHẬP ===")
    # ===== NHÀ CUNG CẤP =====
    print("\n📦 THÔNG TIN NHÀ CUNG CẤP")
    name = input("Tên NCC (*): ").strip()
    phone = input("SĐT NCC (*): ").strip()
    address = input("Địa chỉ NCC: ").strip()

    if not name:
      print("❌ Tên nhà cung cấp không được để trống")
      return

    if not valid_phone(phone):
      print("❌ SĐT nhà cung cấp không hợp lệ")
      return

    supplier = {
      "name": name,
      "phone": phone,
      "address": address
    }
    
    # ===== KIỂM TRA TRÙNG NCC THEO SĐT =====
    for p in imports:
       old = p.get("supplier", {})
       old_phone = old.get("phone","").strip()
       new_phone = supplier["phone"].strip()

       if old_phone and old_phone == new_phone:
          # cùng SĐT nhưng khác tên hoặc địa chỉ → LỖI
          if old.get("name") != supplier["name"] or old.get("address") != supplier["address"]:
            print("❌ SĐT nhà cung cấp đã tồn tại")
            print("📌 Thông tin đã lưu:")
            print(f"   Tên: {old.get('name')}")
            print(f"   Địa chỉ: {old.get('address')}")
            print("⚠️ Không được phép nhập NCC trùng SĐT nhưng khác thông tin")
            return
          else:
            # cùng SĐT + cùng info → dùng lại NCC cũ
            supplier = old
            break


    if not supplier["name"]:
        print("❌ Tên nhà cung cấp không được để trống")
        return

    import_id = f"PN{len(imports)+1:04d}"

    phieu = {
        "import_id": import_id,
        "supplier": supplier,
        "admin": admin_email,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "items": [],
        "total": 0
    }
# ======================
# XEM DANH SÁCH TQ
# ======================
def view_imports():
    pass

# ======================
# XEM CHI TIẾT
# ======================
def view_import_detail():
    pass
# ======================
# CHỈNH SỬA PHIẾU 
# ======================
def edit_import():
    pass

# ==========================================
# THỐNG KÊ NHẬP HÀNG THEO THÁNG + NHÀ CUNG CẤP
# ==========================================
def stat_by_month():
    pass

# ======================
# MENU
# ======================
def nhaphang_menu(admin_email):
    while True:
        print("\n===📦 NHẬP HÀNG ===")
        print("1. Tạo phiếu nhập")
        print("2. Xem danh sách")
        print("3. Xem chi tiết")
        print("4. Chỉnh sửa phiếu nhập")
        print("5. Thống kê nhập hàng theo tháng")
        print("0. Quay lại")

        c = input("Chọn: ")
        if c == "1":
            create_import(admin_email)
        elif c == "2":
            view_imports()
        elif c == "3":
            view_import_detail()
        elif c == "4":
            edit_import()
        elif c == "5":
            stat_by_month()
        elif c == "0":
            break
