
from typing import Union
from fastapi import APIRouter
router = APIRouter()

from fastapi import FastAPI , status , HTTPException , Depends

from fastapi.params import Body

from random import randrange
import mysql.connector
from .. import models,schema,utils
from ..database import engine,SessionLocal
from sqlalchemy.orm import Session

from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Annotated, List

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

x=Depends(get_db)




@router.post("/user", response_model=schema.return_user)
def create_user(user: schema.user, session: Session = Depends(get_db)):
    hashed_pwd = utils.hash(user.password)
    user_data = user.dict()
    user_data["password"] = hashed_pwd

    new_user = models.User(**user_data)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return new_user



@router.get("/user/{id}", response_model=schema.return_user)
def user_info(id: str, session: Session = Depends(get_db)):
    user = session.get(models.User, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user





        
    