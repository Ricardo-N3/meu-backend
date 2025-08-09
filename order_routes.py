from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependecies import take_session
from eschemas import SchemaOrder
from models import Order

order_router = APIRouter(prefix="/order",tags=["order"])

@order_router.get("/")
async def orders():
    return {"Message": "You have accessed the order route"}

@order_router.post("/order")
async def order_create(order_schema: SchemaOrder, session: Session = Depends(take_session)):
    new_order = Order(user= order_schema.users_id)
    session.add(new_order)
    session.commit()
    return {"message": f"Order created successfully. ID order {new_order.id}"}