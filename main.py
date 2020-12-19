from fastapi import FastAPI, HTTPException
import datetime

from database.user_db import UserInDB
from database.user_db import get_user, save_user
from models.user_models import UserIn, UserNew, UserOut
from fastapi.middleware.cors import CORSMiddleware

api = FastAPI()


origins = [
    "http://localhost.tiangolo.com", 
    "https://localhost.tiangolo.com",
    "http://localhost", 
    "http://localhost:8080",
    "https://dinerall-app.herokuapp.com",
]

api.add_middleware(
    CORSMiddleware, allow_origins=origins,
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

@api.get("/")
async def read_root():
    return "Hola, bienvenidx a Dinerall."

@api.post("/user/auth/")
async def auth_user(user_in: UserIn):

    user_in_db = get_user(user_in.mail)

    if user_in_db == None:
        raise HTTPException(status_code=404, detail="No existe un regristado con el correo electrónico")

    if user_in_db.password != user_in.password:
        return False
    else:
        return True


@api.post("/user/signup/")
async def create_user(user_new: UserNew):

    user_in_db = get_user(user_new.mail)
    if user_in_db != None:
        raise HTTPException(status_code=404, detail="El email ya está registrado.")

    user_new = save_user(user_new)
    user_out = UserOut(**user_new.dict())
    return user_out