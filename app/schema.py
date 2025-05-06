from pydantic import BaseModel,conint

class return_user(BaseModel):
    id:int   
class ReturnUser(BaseModel):
    id: int
    username: str

    
    model_config = {
        "from_attributes": True
    } 


class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    user_id: int
   
    votes_count: int

    class Config:
        orm_mode = True

class Postss(BaseModel):
    title: str
    published: bool =True
    content: str
    
    model_config = {
        "from_attributes": True
    }

class return_post(Postss):
    title:str
    content: str
    id: int
    owner: ReturnUser

class user(BaseModel):
    username: str
    email: str
    password: str
    
    model_config = {
        "from_attributes": True
    }



class UserLogin(BaseModel):
    username: str
    password: str
    
    model_config = {
        "from_attributes": True
    }





class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: int | None = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)