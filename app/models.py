from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from .database import Base


class Post(Base):
    __tablename__ = "post"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(255), nullable=False)  # Set length for title
    content = Column(String(1000), nullable=False)  # Set length for content
    published = Column(Boolean, server_default=text("TRUE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("NOW()"))
     
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner= relationship("User")

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    phone_num = Column(String(255), nullable=False)


class Vote(Base):
    __tablename__="votes"
    user_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),primary_key=True)
    post_id=Column(Integer,ForeignKey("post.id",ondelete="CASCADE"),primary_key=True)