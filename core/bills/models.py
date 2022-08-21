from tkinter import CASCADE
from xmlrpc.client import Boolean
from sqlalchemy import Column, String, Integer, TIMESTAMP, ForeignKey
from core.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from fastapi_utils.guid_type import GUID







class Contract(Base):
    __tablename__ = "contract_agreement"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    slug = Column(String, nullable=False, unique = True)
    day = Column(Integer, nullable= False)
    duration = Column(Integer, nullable=False)
    total_amount = Column(Integer, nullable= False)
    scheduled_amount = Column(Integer, nullable = False)
    second_party_id = Column(ForeignKey("users.id", ondelete=CASCADE))
    frist_party_id = Column(ForeignKey("users.id", ondelete=CASCADE))
    first_party_acceptance = Column(Boolean, server_default= text("true")),
    second_party_acceptance = Column(Boolean, server_default= text("false")),
    date_created = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    user = relationship("users")




# class BillTransactions(Base):
#     __tablename__ = "bill_transactions"
#     id = Column(GUID, primary_key =True)
#     bill_id=  Column(ForeignKey("bills.id", ondelete="CASCADE"))




