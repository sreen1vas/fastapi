

from fastapi import FastAPI 
from . import models
from .database import engine,SessionLocal

from fastapi.middleware.cors import CORSMiddleware


from .Routes import post,user,login,vote
 
  # Ensure your model is correctly imported


# Ensure models are created before the app runs
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(post.router)
app.include_router(user.router)

app.include_router(login.router)
app.include_router(vote.router)
