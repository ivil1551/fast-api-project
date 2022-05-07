from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.controller import user_controller, tweet_controller

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router=user_controller.user_router, prefix='/api/v1/user')
app.include_router(router=tweet_controller.tweet_router, prefix='/api/v1/tweet')
