from fastapi import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
router = APIRouter()
from typing import Optional
from fastapi import FastAPI , status , HTTPException , Depends

import mysql.connector
from .. import models,schema
from ..database import engine,SessionLocal,get_db
from sqlalchemy.orm import Session

from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Annotated, List
from . import OAuth2



@router.post("/vote")
def vote(vote:schema.Vote,userid: Annotated[int, Depends(OAuth2.get_current_user)],db:  Session = Depends(get_db)):
    vote_query=db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id== userid.id)
    found_vote=vote_query.first()
    if (vote.dir==1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Already Voted")

        new_vote=models.Vote(post_id=vote.post_id,user_id=userid.id)
        db.add(new_vote)
        db.commit()
        return{"message":"successfully voted"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message":"deleted successfully"}