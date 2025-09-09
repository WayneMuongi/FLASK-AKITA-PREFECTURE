import os
from dotenv import load_dotenv

#loading enviromental vairables

load_dotenv()
print(os.getenv("DATABASE_URL"))

class Config:
    SQLALCHEMY_DATABASE_URI=os.getenv("DATABASE_URL")
    SQLACHEMY_TRACK_MODIFICATIONS=False
    SECRET_KEY="secret"