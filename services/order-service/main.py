from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

orders_db = {}

class Order(BaseModel):
    user_id: int
    product_name: str
    quantity: int

@app.get("/")
def health():
    return {"status": "order service is running"}

@app.post("/orders")
def create_order(order: Order):

    order_id = len(orders_db) + 1

    orders_db[order_id] = {
        "id": order_id,
        "user_id": order.user_id,
        "product_name": order.product_name,
        "quantity": order.quantity,
        "status": "created"
    }

    return orders_db[order_id]

@app.get("/orders/{order_id}")
def get_order(order_id: int):

    order = orders_db.get(order_id)

    if not order:
        return {"error": "order not found"}

    return order

@app.get("/orders")
def get_orders():
    return list(orders_db.values())

