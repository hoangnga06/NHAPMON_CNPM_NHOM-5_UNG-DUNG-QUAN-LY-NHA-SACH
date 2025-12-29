import json
import os
from datetime import datetime
from openpyxl import Workbook
from openpyxl import load_workbook

BOOK_FILE = "books.json"
SALE_FILE = "sales.json"

# ======================
# LOAD DATA
# ======================
def load_books():
    if not os.path.exists(BOOK_FILE):
        return {}
    with open(BOOK_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def load_sales():
    if not os.path.exists(SALE_FILE):
        return []
    with open(SALE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# =================================================
# BÁO CÁO TỒN KHO
# =================================================
def report_inventory():
    books = load_books()
    if not books:
        print("❌ Chưa có dữ liệu sách")
        return

    # Gom sách theo thể loại
    categories = {}
    for bid, b in books.items():
        cat = b.get("category", "KHÁC").upper()
        categories.setdefault(cat, [])
        categories[cat].append((bid, b))

    # Sắp xếp thể loại theo ABC
    for cat in sorted(categories.keys()):
        print("\n" + "=" * 100)
        print(f"📚 THỂ LOẠI: {cat}")
        print("=" * 100)
        print("{:<8} {:<30} {:<10} {}".format(
            "Mã", "Tên sách", "Tồn", "Cảnh báo"
        ))
        print("-" * 100)

        for bid, b in categories[cat]:
            qty = b.get("qty", 0)
            warn = "⚠️ Tồn thấp" if qty < 5 else ""
            print("{:<8} {:<30} {:<10} {}".format(
                bid,
                b.get("name", ""),
                qty,
                warn
            ))
# =================================================
# BÁO CÁO DOANH THU
# =================================================
def report_revenue():
    sales = load_sales()
    if not sales:
        print("❌ Chưa có dữ liệu bán hàng")
        return

    stats = {}

    for s in sales:
        date = s["time"].split(" ")[0]   # dd/mm/yyyy
        stats.setdefault(date, 0)
        stats[date] += s.get("pay", 0)

    print("\n💰 BÁO CÁO DOANH THU THEO NGÀY")
    print("-" * 40)
    for d in sorted(stats):
        print(f"{d}: {stats[d]:,.0f} đ")
def report_revenue_by_month():
    sales = load_sales()
    if not sales:
        print("❌ Chưa có dữ liệu bán hàng")
        return

    stats = {}

    for s in sales:
        # time: dd/mm/yyyy hh:mm
        d = datetime.strptime(s["time"], "%d/%m/%Y %H:%M")
        key = d.strftime("%m/%Y")  # tháng/năm
        stats.setdefault(key, 0)
        stats[key] += s.get("pay", 0)

    print("\n💰 BÁO CÁO DOANH THU THEO THÁNG")
    print("-" * 40)
    for k in sorted(stats):
        print(f"{k}: {stats[k]:,.0f} đ")
def report_revenue_by_year():
    sales = load_sales()
    if not sales:
        print("❌ Chưa có dữ liệu bán hàng")
        return

    stats = {}

    for s in sales:
        d = datetime.strptime(s["time"], "%d/%m/%Y %H:%M")
        year = d.year
        stats.setdefault(year, 0)
        stats[year] += s.get("pay", 0)

    print("\n💰 BÁO CÁO DOANH THU THEO NĂM")
    print("-" * 40)
    for y in sorted(stats):
        print(f"{y}: {stats[y]:,.0f} đ")

# =================================================
# XUẤT EXCEL
# =================================================

EXCEL_FILE = "BAOCAO_TONKHO.xlsx"

def update_inventory_excel():
    pass
# =================================================
# MENU BÁO CÁO (ADMIN)
# =================================================
def menu_baocao():
    while True:
        print("\n=== 📊 MENU BÁO CÁO ===")
        print("1. Xem báo cáo tồn kho (console)")
        print("2. Xem doanh thu (console)")
        print("3. Xuất BÁO CÁO TỔNG HỢP (Excel)")
        print("0. Quay lại")

        ch = input("Chọn: ")

        if ch == "1":
            report_inventory()

        elif ch == "2":
            print("\n--- DOANH THU ---")
            report_revenue()
            report_revenue_by_month()
            report_revenue_by_year()

        elif ch == "3":
            export_all_report_excel_one_sheet()# ✅ FILE TỔNG HỢP DUY NHẤT

        elif ch == "0":
            break
        else:
            print("❌ Lựa chọn không hợp lệ")
