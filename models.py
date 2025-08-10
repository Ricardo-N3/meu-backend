from sqlalchemy import create_engine,Column,String, Integer, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils.types import ChoiceType

db = create_engine("sqlite:///data.db")

Base = declarative_base()

#base de dados
class User(Base):
    __tablename__ = "users"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String)
    email = Column("email", String, nullable=False)
    passwords = Column("passwords", String)
    active = Column("active", Boolean)
    admin = Column("admin", Boolean, default=False)

    def __init__(self, name, email, passwords, active=True, admin=False):
        self.name = name
        self.email = email
        self.passwords = passwords
        self.active = active
        self.admin = admin

#pedidos
class Order(Base):
    __tablename__ = "orders"

   # ORDER_STATUS = (
    #    ("PENDING", "PENDING"),
    #    ("CANCELLED", "CANCELLED"),
   #     ("FINISHED", "FINISHED")
    #)

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    status = Column("status", String)
    user = Column("user", ForeignKey("users.id"))
    cost = Column("cost", Float)
#    itens = 

    def __init__(self, user, status = "PENDING", cost = 0):
        self.user = user
        self.cost = cost
        self.status = status

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    quantity = Column("quantity", Integer)
    flavor = Column("flavor", String)
    size = Column("size",String)
    unitary_cost = Column("unitary_cost", Float)
    order = Column("order", ForeignKey("orders.id"))

    def __init__(self, quantity, flavor, size, unitary_cost, order):
        self.quantity = quantity
        self.flavor = flavor
        self.size = size
        self.unitary_cost = unitary_cost
        self.order = order