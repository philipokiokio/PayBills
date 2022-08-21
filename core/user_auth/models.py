from enum import unique
from sqlalchemy import Column, String, Integer,ForeignKey ,Boolean, TIMESTAMP
from core.database import  Base
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique= True, nullable= False)
    username= Column(String, unique= True, nullable=False)
    first_name = Column(String,nullable=False)
    last_name = Column(String, nullable= False)
    phone_number = Column(String, nullable= True)
    password = Column(String, nullable=False)
    is_verified= Column(Boolean, default = False, nullable= False)
    is_invited = Column(Boolean, default = False, nullable= False)
    super_user =  Column(Boolean, default = False, nullable= False)
    terms_of_service =  Column(Boolean, default = False, nullable= False)
    date_joined = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    
class ContractualInvites(Base):
    __tablename__ ="contractual_invites"
    id = Column(Integer,primary_key = True,index = True)
    inviter_id = Column(ForeignKey("users.id", ondelete="CASCADE"))
    confirmation = Column(Boolean, server_Default = text("false"))
    email_invited = Column(String, nullable=False, unique=True)
    date_created = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    user = relationship("users")

    
# class User_KYC(Base):
#     __tablename__ = "users-kyc"
#     id = Column(Integer, primary_key=True, index=True)

#     user_id = Column(Integer,ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
#     created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
#     user= relationship(User)