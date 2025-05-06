from fastapi import FastAPI , status , HTTPException , Depends , Query

from fastapi import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from .. import models,schema,utils
from . import OAuth2
from ..database import engine,SessionLocal
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
router = APIRouter()



@router.post("/login",response_model=schema.Token)  # Use appropriate schema
def login(    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: Session = Depends(get_db)):
    stmt = select(models.User).where(models.User.username == form_data.username)
    result = session.execute(stmt)
    user = result.scalars().first()

    if not user or not utils.pwd_check(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    tock = OAuth2.create_access_token({"userid": user.id})

    
    return {"access_token": tock, "token_type": "bearer"}




