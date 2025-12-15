from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Cho phép frontend gọi API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Fake database
books = [
    {"id": 1, "ten": "Doremon", "tac_gia": "Fujiko F Fujio", "gia": 20000, "so_luong": 10},
    {"id": 2, "ten": "Sherlock Holmes", "tac_gia": "Conan Doyle", "gia": 50000, "so_luong": 5},
]

customers = []

@app.get("/books")
def get_books():
    return {"status": True, "data": books}

@app.post("/customer")
def add_customer(khach: dict):
    for c in customers:
        if c["sdt"] == khach["sdt"]:
            return {"status": False, "message": "Số điện thoại đã tồn tại!"}

    customers.append(khach)
    return {"status": True, "message": "Thêm khách hàng thành công!"}

@app.get("/customer/search")
def search_customer(keyword: str):
    kq = [c for c in customers if keyword.lower() in c["ten"].lower() or keyword in c["sdt"]]
    return {"status": True, "data": kq}
