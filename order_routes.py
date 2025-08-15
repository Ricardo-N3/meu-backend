from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependecies import take_session, verification_token
from eschemas import SchemaOrder, OrderItemSchema, ResponseOrderSchema
from models import Order, User, OrderItem

order_router = APIRouter(prefix="/order",tags=["order"], dependencies=[Depends(verification_token)])

@order_router.get("/")
async def orders():
    return {"Message": "You have accessed the order routes"}

@order_router.post("/order")
async def order_create(order_schema: SchemaOrder, session: Session = Depends(take_session)):
    user = session.query(User).filter(User.id==order_schema.users_id).first()
    if not user:
        raise HTTPException(status_code=400, detail="User not found or user does not exist")
    else:
        new_order = Order(user=user.id)
        session.add(new_order)
        session.commit()
        return {"message": f"Order created successfully. ID order {new_order.id}"}

@order_router.post("/order/cancel/{order_id}")
async def cancel_order(order_id: int, session: Session = Depends(take_session), user: User = Depends(verification_token)):
    order = session.query(Order).filter(Order.id==order_id).first()
    if not order:
         raise HTTPException(status_code=400,detail="Request not found")
    if not user.admin and user.id != order.user:
        raise HTTPException(status_code=403,detail="You are not allowed to cancel the order")
    if order.status in ["CANCELED"]:
        raise HTTPException(status_code=400, detail=f"Order is alredy {order.status.lower()}")
    order.status = "CANCELED"
    session.commit()
    return {
        "message":f"Order {order.id} successfully canceled",
        "Order":order
    }

@order_router.post("/order/finished/{order_id}")
async def finished_order(order_id: int, session: Session = Depends(take_session), user: User = Depends(verification_token)):
    order = session.query(Order).filter(Order.id==order_id).first()
    if not order:
        raise HTTPException(status_code=400, detail="Request not found")
    if not user.admin:
        raise HTTPException(status_code=403, detail="Only admins can finish orders")
    if order.status in ["CANCELED","FINISHED"]:
        raise HTTPException(status_code=400, detail=f"Order is alredy {order.status.lower()}")
    order.status = "FINISHED"
    session.commit()
    return {
        "message":f"Order {order.id} successfully finished",
        "Order":order
    }

@order_router.get("/list")
async def order_list(session: Session = Depends(take_session), user: User = Depends(verification_token)):
    if not user.admin:
        raise HTTPException(status_code=403, detail="Only admins can make this operation")
    else:
        orders = session.query(Order).all()
    return {
        "Orders": orders
    }

@order_router.post("/order/item-add/{order_id}")
async def add_order_item(order_id: int,order_item_schema: OrderItemSchema, session: Session = Depends(take_session), user: User = Depends(verification_token)):
    order = session.query(Order).filter(Order.id==order_id).first()
    if not order:
        raise HTTPException(status_code=400, detail="Request not found")
    if not user.admin and user.id != order.user:
        raise HTTPException(status_code=403, detail="You are not allowed to add items to this order")
    else:
        order_item = OrderItem(order_item_schema.quantity, order_item_schema.flavor, order_item_schema.size, order_item_schema.unitary_cost, order_id)
        session.add(order_item)
        order.cost_calculator()
        session.commit()
        return {
            "message":"Item created successfully",
            "id_item": order_item.id,
            "Cost_order": order.cost
        }
    
@order_router.post("/order/item-remove/{order_item_id}")
async def remove_order_item(order_item_id: int, session: Session = Depends(take_session), user: User = Depends(verification_token)):
    order_item = session.query(OrderItem).filter(OrderItem.id==order_item_id).first()
    order = session.query(Order).filter(Order.id==order_item.order).first()
    if not order_item:
        raise HTTPException(status_code=400, detail="Item in order not found")
    if not user.admin and user.id != order.user:
        raise HTTPException(status_code=403, detail="You are not allowed to add items to this order")
    else:
        session.delete(order_item)
        order.cost_calculator()
        session.commit()
        return {
            "message": "Item in order removed successfully",
            "order_itens_quantity": len(order.itens),
            "Order": order
        }
    
@order_router.get("/order/{order_id}", response_model= ResponseOrderSchema)
async def order_viewer(order_id: int, session: Session = Depends(take_session), user: User = Depends(verification_token)):
    order = session.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=400, detail="Order not found")
    if not user.admin and user.id != order.user:
        raise HTTPException(status_code=403, detail="You do not have permission to make this modification")
    return {
        "order_itens_quantity": len(order.itens),
        "Order":order
    }

@order_router.get("/list/{user_id}", response_model= list[ResponseOrderSchema])
async def order_list(session: Session = Depends(take_session), user: User = Depends(verification_token)):
    orders = session.query(Order).filter(Order.user == user.id).all()
    return orders