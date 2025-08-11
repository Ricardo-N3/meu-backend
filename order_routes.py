from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependecies import take_session, verification_token
from eschemas import SchemaOrder
from models import Order, User

order_router = APIRouter(prefix="/order",tags=["order"], dependencies=[Depends(verification_token)])

@order_router.get("/")
async def orders():
    return {"Message": "You have accessed the order routes"}

@order_router.post("/order")
async def order_create(order_schema: SchemaOrder, session: Session = Depends(take_session)):
    new_order = Order(user=order_schema.users_id)
    session.add(new_order)
    session.commit()
    return {"message": f"Order created successfully. ID order {new_order.id}"}

@order_router.post("/order/cancel/{order_id}")
async def cancel_order(order_id: int, session: Session = Depends(take_session), user: User = Depends(verification_token)):
    order = session.query(Order).filter(Order.id==order_id).first()
    if not order:
         raise HTTPException(status_code=400,detail="Request not found")
    if not user.admin and user.id != order.user:
        raise HTTPException(status_code=401,detail="You are not allowed to cancel the order")
    order.status = "CANCELED"
    session.commit()
    return {
        "message":f"Order {order_id} successfully canceled",
        "Order":order
    }

# @order_router.post("/order/finished/{order_id}")
# async def finished_order(order_id: int, session: Session = Depends(take_session)):
#     order = session.query(Order),filter(Order.id==order_id).first()
#     if not order:
#         raise HTTPException(status_code=400, detail="request not found")
#     order.status = "FINISHED"
#     session.commit()
#     return {
#         "message":f"Order {order_id} successfully finished",
#         "Order":order
#     }
