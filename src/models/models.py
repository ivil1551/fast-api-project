# this pydantic base model will helps to handle input data validation in fastAPI framework level
from pydantic import BaseModel


class CreateTweet(BaseModel):
    user_id: int
    tweet: str


class DeleteTweet(BaseModel):
    user_name: str


class CreateUser(BaseModel):
    user_name: str
