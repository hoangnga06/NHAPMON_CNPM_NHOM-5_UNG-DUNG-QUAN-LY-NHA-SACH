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
    # ===== THÊM SÁCH =====
    while True:
      print("\n➕ THÊM SÁCH VÀO PHIẾU")

      keyword = input("Nhập tên sách: ").strip()
      if not keyword:
        print("❌ Tên sách không được để trống")
        continue

      matches = search_books_by_name(books, keyword)
      book_id = None

      # --- CÓ SÁCH TƯƠNG TỰ ---
      if matches:
        selected = choose_existing_book(matches)

        if selected == "INVALID":
            continue
        elif selected:
            book_id = selected

      # --- THÊM SÁCH MỚI ---
      if not book_id:
        book_id = SACH.generate_next_book_id(books)
        print(f"🆔 Mã sách tự động: {book_id}")

        book_name = input("Tên sách đầy đủ (*): ").strip()
        if not book_name:
            print("❌ Tên sách không được để trống")
            continue

        author = input("Tác giả: ").strip()
        category = input("Thể loại: ").strip()

        try:
            price_sell = float(input("Giá bán (*): "))
            if price_sell <= 0:
                raise ValueError
        except:
            print("❌ Giá bán không hợp lệ")
            continue

        books[book_id] = {
            "name": book_name,
            "author": author,
            "category": category,
            "price": price_sell,
            "qty": 0
        }

      b = books[book_id]
      print(f"\n📘 ĐANG NHẬP: {b['name']} [{book_id}]")

      # --- THÔNG TIN NHẬP ---
      try:
        qty = int(input("Số lượng nhập: "))
        price = float(input("Giá nhập: "))
        if qty <= 0 or price <= 0:
            raise ValueError
      except:
        print("❌ Số lượng hoặc giá không hợp lệ")
        continue

      found = False
      for item in phieu["items"]:
        if item["book_id"] == book_id:
            item["qty"] += qty
            item["subtotal"] += qty * price
            found = True
            break

      if not found:
        phieu["items"].append({
            "book_id": book_id,
            "qty": qty,
            "price": price,
            "subtotal": qty * price
        })

      phieu["total"] += qty * price
      books[book_id]["qty"] += qty

      if input("Thêm sách khác? (y/n): ").lower() != "y":
        break


    if not phieu["items"]:
        print("❌ Phiếu nhập không có sách – huỷ tạo")
        return

    imports.append(phieu)
    save_imports(imports)
    SACH.save_books(books)

    print(f"✅ Đã tạo phiếu nhập {import_id}")                                  
# ======================
# XEM DANH SÁCH TQ
# ======================
def view_imports():
    imports = load_imports()

    if not imports:
        print("📭 Chưa có phiếu nhập nào")
        return

    print("\n=== DANH SÁCH PHIẾU NHẬP ===")
    print("{:<10} {:<25} {:<20} {:>15}".format(
        "Mã phiếu", "Nhà cung cấp", "Ngày", "Tổng tiền"
    ))
    print("-" * 75)

    for p in imports:
        s = p.get("supplier", {})
        print("{:<10} {:<25} {:<20} {:>15}".format(
            p.get("import_id", ""),
            s.get("name", "❓"),
            p.get("created_at", ""),
            f"{p.get('total', 0):,}đ"
           
        ))
# ======================
# XEM CHI TIẾT
# ======================
def view_import_detail():
    pid = input("Nhập mã phiếu: ")
    imports = load_imports()
    books = SACH.load_books()

    p = next((x for x in imports if x["import_id"] == pid), None)
    if not p:
        print("❌ Không tìm thấy")
        return
    s = p.get("supplier",{})
    print(f"\n PHIẾU {pid}")
    print(f" NCC: {s.get('name','')}")
    print(f" SĐT: {s.get('phone','')}")
    print(f" Địa chỉ: {s.get('address','')}")
    print(f" Ngày nhập: {p['created_at']}")
    print("-" * 90)


    print("{:<8} {:<25} {:<15} {:<12} {:<8} {:<12}".format(
        "Mã", "Tên sách", "Thể loại", "Giá nhập", "SL", "Thành tiền"
    ))
    print("-" * 90)
    for i in p["items"]:
        bid = i["book_id"]
        b = books.get(bid, {})

        print("{:<8} {:<25} {:<15} {:<12} {:<8} {:<12}".format(
            bid,
            b.get("name", "❓"),
            b.get("category", ""),
            f"{i['price']:,}",
            i["qty"],
            f"{i['subtotal']:,}"
        ))

    print("-" * 90)
    print(f"💰 TỔNG TIỀN: {p['total']:,}đ")
# ======================
# CHỈNH SỬA PHIẾU 
# ======================
def edit_import():
    pid = input(" ✏️ Nhập mã phiếu cần sửa: ")
    imports = load_imports()
    books = SACH.load_books()
    # TÌM PHIẾU
    p = next((x for x in imports if x["import_id"] == pid), None)
    if not p:
        print("❌ Không tìm thấy phiếu")
        return

    print(f"\n=== ✏️ CHỈNH SỬA PHIẾU {pid} ===")
    s = p.get("supplier", {})
    print(f"Nhà cung cấp: {s.get('name','')}")
    print(f"Ngày nhập: {p['created_at']}")
    print("-" * 60)
    # ===== CHỈNH THÔNG TIN NHÀ CUNG CẤP =====
    print("\n--- ✏️ Chỉnh thông tin nhà cung cấp ---")
    new_name = input(f"Tên NCC [{s.get('name','')}]: ").strip()
    new_phone = input(f"SĐT [{s.get('phone','')}]: ").strip()
    new_addr = input(f"Địa chỉ [{s.get('address','')}]: ").strip()

    # nếu bỏ trống thì giữ nguyên
    if new_name:
       s["name"] = new_name

    if new_phone:
       # kiểm tra SĐT: bắt đầu bằng 0, đủ 10 số
       if not (new_phone.isdigit() and new_phone.startswith("0") and len(new_phone) == 10):
          print("❌ SĐT NCC không hợp lệ (phải bắt đầu bằng 0 và đủ 10 số)")
          return
       s["phone"] = new_phone

    if new_addr:
       s["address"] = new_addr

    p["supplier"] = s


    # lưu số lượng cũ
    old_items = {i["book_id"]: i["qty"] for i in p["items"]}

    new_items = {}

    # ===== NHẬP LẠI SỐ LƯỢNG =====
    for i in p["items"]:
       bid = i["book_id"]
       b = books.get(bid, {})
       old_qty = i["qty"]

       print(f"\n📘 {bid} - {b.get('name','')}")
       print(f"   SL cũ: {old_qty}")
       raw = input("   SL mới (Enter = giữ nguyên): ").strip()

       if raw == "":
          new_qty = old_qty
       else:
          try:
            new_qty = int(raw)
            if new_qty < 0:
               raise ValueError
          except:
             print("❌ Số lượng không hợp lệ")
             return

       new_items[bid] = new_qty


    

    new_items[bid] = new_qty

 


    # ===== KIỂM TRA KHO TRƯỚC KHI ÁP DỤNG =====
    for bid in old_items:
        diff = new_items[bid] - old_items[bid]

        # nếu giảm SL mà kho không đủ → cấm
        if diff < 0:
            if bid not in books or books[bid]["qty"] < abs(diff):
                print("❌ Không thể chỉnh sửa – tồn kho không đủ")
                print(f"   Sách {bid}: kho hiện tại {books.get(bid,{}).get('qty',0)}")
                return

    # ===== ÁP DỤNG ĐIỀU CHỈNH KHO =====
    for bid in old_items:
        diff = new_items[bid] - old_items[bid]
        books[bid]["qty"] += diff

    # ===== CẬP NHẬT PHIẾU =====
    for i in p["items"]:
        bid = i["book_id"]
        i["qty"] = new_items[bid]
        i["subtotal"] = i["qty"] * i["price"]

    p["total"] = sum(i["subtotal"] for i in p["items"])

    save_imports(imports)
    SACH.save_books(books)

    print("✅ Đã chỉnh sửa phiếu nhập & cập nhật tồn kho thành công")



# ==========================================
# THỐNG KÊ NHẬP HÀNG THEO THÁNG + NHÀ CUNG CẤP
# ==========================================
def stat_by_month():
    imports = load_imports()

    if not imports:
        print("📭 Chưa có dữ liệu nhập hàng")
        return

    stats = {}

    for p in imports:
        month = p["created_at"][:7]   # YYYY-MM
        s = p.get("supplier", {})
        sname = s.get("name", "❓")

        if month not in stats:
            stats[month] = {}

        if sname not in stats[month]:
            stats[month][sname] = {
                "count": 0,
                "total": 0
            }

        stats[month][sname]["count"] += 1
        stats[month][sname]["total"] += p["total"]

    print("\n📊 THỐNG KÊ NHẬP HÀNG THEO THÁNG + NCC")

    for month in sorted(stats.keys()):
        print(f"\n📅 Tháng: {month}")
        print("-" * 60)
        print("{:<25} {:<10} {:>15}".format(
            "Nhà cung cấp", "Số phiếu", "Tổng tiền"
        ))
        print("-" * 60)

        month_total = 0

        for sname, v in stats[month].items():
            print("{:<25} {:<10} {:>15}".format(
                sname,
                v["count"],
                f"{v['total']:,}đ"
            ))
            month_total += v["total"]

        print("-" * 60)
        print(f"➡️ TỔNG THÁNG {month}: {month_total:,}đ")

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
