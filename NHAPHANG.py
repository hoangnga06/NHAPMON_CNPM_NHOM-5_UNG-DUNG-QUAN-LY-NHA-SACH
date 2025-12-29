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
    pass
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
