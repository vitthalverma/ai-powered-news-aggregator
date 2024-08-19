from fastapi import FastAPI
from app import models
from app.database import engine
from fastapi.middleware.cors import CORSMiddleware
from app.router import news, user


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(news.router)
app.include_router(user.router)



@app.get("/")
async def root():
    return {"message": "Welcome to the AI-powered News Aggregator!"}