from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .config import settings
from .database import engine
from .routers import post, user, auth, vote

# Commented below as it is being handles by alembic
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# origins = [
#     "https://www.google.com",
#     "https://www.youtube.com"
# ]
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)



@app.get("/")
async def root():
    return {"message": "This is my API"}






