from flask import Flask, jsonify

app = Flask(__name__)

# Route trang chủ
@app.route("/")
def home():
    return jsonify({"message": "Backend Flask chạy thành công!"})

# Route xem danh sách sản phẩm
@app.route("/products")
def get_products():
    sample_products = [
        {"id": 1, "name": "Sách A", "price": 50000},
        {"id": 2, "name": "Sách B", "price": 75000},
    ]
    return jsonify(sample_products)

if __name__ == "__main__":
    app.run(debug=True)
