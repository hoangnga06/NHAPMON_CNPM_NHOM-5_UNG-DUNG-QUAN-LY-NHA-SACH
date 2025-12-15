from flask import Flask, request, jsonify

app = Flask(__name__)

# ==========================
#  API TEST – kiểm tra server
# ==========================
@app.get("/")
def home():
    return {"message": "Backend Flask chạy thành công!"}


# =====================================
#  API THÊM KHÁCH HÀNG (ví dụ bạn đã có)
# =====================================
customers = []

@app.post("/customer/add")
def add_customer():
    data = request.json

    # Kiểm tra thiếu thông tin
    if not data.get("name") or not data.get("phone"):
        return jsonify({"status": False, "message": "Thiếu thông tin!"})

    # Kiểm tra trùng SĐT
    for c in customers:
        if c["phone"] == data["phone"]:
            return jsonify({"status": False, "message": "Số điện thoại đã tồn tại!"})

    customers.append(data)
    return jsonify({"status": True, "message": "Thêm khách hàng thành công"})


# =====================================
#  API TÌM KIẾM
# =====================================
@app.get("/customer/search")
def search_customer():
    keyword = request.args.get("q", "").lower()
    result = [c for c in customers if keyword in c["name"].lower() or keyword in c["phone"]]
    return jsonify({"status": True, "data": result})


# ====================
#  CHẠY SERVER
# ====================
if __name__ == "__main__":
    app.run(debug=True)
