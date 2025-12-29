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
    pass

# =================================================
# BÁO CÁO DOANH THU
# =================================================
def report_revenue():
    pass

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
