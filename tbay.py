from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship

    
engine = create_engine('postgresql://ubuntu:thinkful@localhost:5432/tbay')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()



class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    start_time = Column(DateTime, default=datetime.utcnow)
    
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    bids = relationship("Bid", backref="item")
    
class User(Base):
    __tablename__="users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    
    auction_items = relationship("Item", backref="owner")
    bid=relationship("Bid", backref="owner")
    
class Bid(Base):
    __tablename__="bids"
    
    id = Column(Integer, primary_key=True)
    price = Column(Float, nullable=False)

    item_id = Column(Integer, ForeignKey('items.id'), nullable=False)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
Base.metadata.create_all(engine)

alice = User(username='Alice', password='thinkful')
jorge = User(username='Jorge', password='thinkful')
sooraj = User(username='Sooraj', password='thinkful')

baseball= Item(name='baseball', description='A baseball from a famous star', owner=alice)

jorge_bid = Bid(price=10, item=baseball, owner=jorge)
sooraj_bid= Bid(price=11, item=baseball, owner=sooraj)

session.add_all([alice, jorge, sooraj, baseball, jorge_bid, sooraj_bid])
session.commit()

print('Alice auction items:')
for item in alice.auction_items:
    print(item.name)

print('Users bid on baseball are:')
for bid in baseball.bids:
    print(bid.owner.username)
    
print("Owner for the baseball is:{}".format(baseball.owner.username))

print("Bids placed on items are:")
for bid in baseball.bids:
    print(bid.price)