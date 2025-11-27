from flask import Flask, request, redirect, render_template_string

app = Flask(__name__)

# Danh sách sản phẩm (không dùng JSON)
products = [
    {"id": 1, "ten": "Chuột", "gia": 150000, "loai": "Thiết bị", "sl": 10},
    {"id": 2, "ten": "Bàn phím", "gia": 300000, "loai": "Thiết bị", "sl": 5}
]

# HTML gọn nhất
page = """
<h2>Danh sách sản phẩm</h2>
<ul>
{% for p in products %}
    <li>
        {{p.ten}} - {{p.gia}}đ - SL: {{p.soluong}}
        <a href="/update/{{p.id}}">[Sửa]</a>
    </li>
{% endfor %}
</ul>

{% if product %}
<hr>
<h3>Sửa sản phẩm</h3>

<form method="POST">
    Tên: <input name="ten" value="{{product.ten}}"><br><br>
    Giá: <input name="gia" value="{{product.gia}}" type="number"><br><br>
    Loại: <input name="loai" value="{{product.loai}}"><br><br>
    Số lượng: <input name="soluong" value="{{product.soluong}}" type="number"><br><br>

    <button type="submit">Lưu</button>
</form>

{% if error %}
<p style="color:red">{{error}}</p>
{% endif %}
{% endif %}
"""

@app.route("/")
def index():
    return render_template_string(page, products=products, product=None)

@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    product = next((p for p in products if p["id"] == id), None)
    error = None

    if request.method == "POST":
        ten = request.form["ten"]
        gia = request.form["gia"]
        loai = request.form["loai"]
        soluong = request.form["soluong"]

        # Ràng buộc đơn giản
        if ten == "":
            error = "Tên không được để trống"
        elif int(gia) <= 0:
            error = "Giá phải > 0"
        elif int(soluong) < 0:
            error = "Sl phải ≥ 0"
        else:
            product["ten"] = ten
            product["gia"] = int(gia)
            product["loai"] = loai
            product["soluong"] = int(soluong)
            return redirect("/")

    return render_template_string(page, products=products, product=product, error=error)

if __name__ == "__main__":
    app.run(debug=True)
