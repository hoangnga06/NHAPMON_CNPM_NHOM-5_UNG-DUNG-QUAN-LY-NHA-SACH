# Danh sách lưu sách
danh_sach_sach = []

def them_sach(ma_sach, ten_sach, tac_gia, the_loai, gia, so_luong, mo_ta=""):
    # ---- KIỂM TRA DỮ LIỆU ----
    
    # 1. Kiểm tra trống
    if not ma_sach or not ten_sach or not tac_gia or not the_loai:
        return {"status": "error", "message": "Không được để trống các trường bắt buộc."}

    # 2. Kiểm tra mã sách không trùng
    for sach in danh_sach_sach:
        if sach["ma_sach"] == ma_sach:
            return {"status": "error", "message": "Mã sách đã tồn tại!"}

    # 3. Kiểm tra giá
    try:
        gia = float(gia)
        if gia <= 0:
            return {"status": "error", "message": "Giá phải lớn hơn 0."}
    except:
        return {"status": "error", "message": "Giá phải là số."}

    # 4. Kiểm tra số lượng
    try:
        so_luong = int(so_luong)
        if so_luong < 0:
            return {"status": "error", "message": "Số lượng phải ≥ 0."}
    except:
        return {"status": "error", "message": "Số lượng phải là số nguyên."}

    # ---- THÊM SÁCH ----
    sach_moi = {
        "ma_sach": ma_sach,
        "ten_sach": ten_sach,
        "tac_gia": tac_gia,
        "the_loai": the_loai,
        "gia": gia,
        "so_luong": so_luong,
        "mo_ta": mo_ta
    }

    danh_sach_sach.append(sach_moi)

    return {"status": "success", "message": "Thêm sách thành công!", "data": sach_moi}
