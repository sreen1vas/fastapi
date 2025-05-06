
from typing import Union
from fastapi import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
router = APIRouter()
from typing import Optional
from fastapi import FastAPI , status , HTTPException , Depends
from sqlalchemy import func
from fastapi.params import Body

from random import randrange
import mysql.connector
from .. import models,schema
from ..database import engine,SessionLocal
from sqlalchemy.orm import Session

from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import Annotated, List
from . import OAuth2

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


x=Depends(get_db)


@router.get("/")
def read_root():
    return {"Hello": "World"}


@router.get("/posts", response_model=List[schema.PostResponse])


def read_posts(
    session: Session = Depends(get_db),
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
    search: Optional[str] = Query(None)  # Optional search parameter
):
    # Construct query with a join to count votes
    stmt = session.query(
        models.Post,
        func.count(models.Vote.post_id).label('votes_count')
    ).outerjoin(models.Vote, models.Post.id == models.Vote.post_id)

    # Apply search filter if provided
    if search:
        stmt = stmt.filter(models.Post.title.ilike(f"%{search}%"))

    # Group by post id to get vote count per post
    stmt = stmt.group_by(models.Post.id).offset(offset).limit(limit)

    # Execute query and fetch the results
    result = stmt.all()

    # Convert results into a list of PostResponse models
    posts_with_votes = [
        schema.PostResponse(
            id=post.id,
            title=post.title,
            content=post.content,
            published=post.published,
            user_id=post.user_id,
            created_at=post.created_at.isoformat(),
            votes_count=votes_count
        )
        for post, votes_count in result
    ]

    return posts_with_votes


@router.post("/post",response_model=schema.return_post)
def create_post(
    post: schema.Postss, 
    userid: Annotated[int, Depends(OAuth2.get_current_user)],  # non-default first
    session: Session = Depends(get_db)
):
    print(userid)
    print(userid.email)

    new_post = models.Post(**post.dict(), user_id=userid.id)
  # Convert Pydantic model to ORM model
    session.add(new_post)
    session.commit()
    session.refresh(new_post)
    return new_post  # This will be serialized using PostSchema
  
    # cursor.execute(
    #     "INSERT INTO post (title, published, movie) VALUES (%s, %s, %s)",
    #     (post.title, post.published, post.movie),
    # )
    # conn.commit()

    # # Get the last inserted row
    # cursor.execute("SELECT * FROM post WHERE id = LAST_INSERT_ID()")
    # inserted_row = cursor.fetchone()

    # return {"Inserted Row": inserted_row}
    
@router.get("/posts/{id}")
def post(id: int, userid: Annotated[int, Depends(OAuth2.get_current_user)], session: Session = Depends(get_db)):
    post = (
        session.query(models.Post)
        .filter(models.Post.id == id, models.Post.user_id == userid.id)
        .first()
    )
    if not post:
        raise HTTPException(status_code=404, detail="post not found")
    return post



@router.delete("/post/{id}",status_code=status.HTTP_202_ACCEPTED)
def post(id: int, userid: Annotated[int, Depends(OAuth2.get_current_user)], session: Session = Depends(get_db)):
    to_delete = (
    session.query(models.Post)
    .filter(models.Post.id == id)
    .first()
)

    if not to_delete:
        raise HTTPException(status_code=404, detail="Post not found")
    elif userid.id != to_delete.user_id:
        raise HTTPException(status_code=403, detail="refuses to authorize it")
    else:
        session.delete(to_delete)
        session.commit()
        return {"ok": True}


# @router.delete("/post/{id}", status_code=status.HTTP_202_ACCEPTED)
# def delete_post(id: int, session: Session = Depends(get_db)):
#     to_delete = session.get(models.Post, id)
#     if not to_delete:
#         raise HTTPException(status_code=404, detail="Post not found")
    
#     session.delete(to_delete)
#     session.commit()
#     return {"ok": True}

@router.put("/post/{id}")
def update(id:int, userid: Annotated[int, Depends(OAuth2.get_current_user)],  post: schema.Postss):
    cursor.execute("SELECT id FROM post")
    result = cursor.fetchall()  # Fetch all rows
    # Convert result to a list of IDs
    id_list = [row[0] for row in result]
    if id in id_list:
        cursor.execute(
        "UPDATE post SET title = %s, published = %s, movie = %s WHERE id = %s",
        (post.title, post.published, post.movie, id)
         )
    
        conn.commit()
    
        return {"message": f"Post with ID {id} updated successfully"}




        
       
    else :
        raise HTTPException(status_code=404, detail="Post not found")

