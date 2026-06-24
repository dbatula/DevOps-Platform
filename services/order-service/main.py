from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import SessionLocal, engine
from models import Base, OrderDB

Base.metadata.create_all(bind=engine)

app = FastAPI()


class Order(BaseModel):
    user_id: int
    product_name: str
    quantity: int


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def health():
    return {"status": "order service is running"}


@app.post("/orders")
def create_order(order: Order, db: Session = Depends(get_db)):

    db_order = OrderDB(
        user_id=order.user_id,
        product_name=order.product_name,
        quantity=order.quantity,
        status="created"
    )

    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    return {
        "id": db_order.id,
        "user_id": db_order.user_id,
        "product_name": db_order.product_name,
        "quantity": db_order.quantity,
        "status": db_order.status
    }


@app.get("/orders/{order_id}")
def get_order(order_id: int, db: Session = Depends(get_db)):

    order = db.query(OrderDB).filter(OrderDB.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="order not found")

    return {
        "id": order.id,
        "user_id": order.user_id,
        "product_name": order.product_name,
        "quantity": order.quantity,
        "status": order.status
    }


@app.get("/orders")
def get_orders(db: Session = Depends(get_db)):

    orders = db.query(OrderDB).all()

    return [
        {
            "id": order.id,
            "user_id": order.user_id,
            "product_name": order.product_name,
            "quantity": order.quantity,
            "status": order.status
        }
        for order in orders
    ]