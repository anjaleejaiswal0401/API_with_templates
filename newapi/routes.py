from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi_login import LoginManager
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Request,Form,status,Depends
from fastapi.responses import HTMLResponse,RedirectResponse
from pathlib import Path
from fastapi import FastAPI
from fastapi import APIRouter
from . models import *
from passlib.context import CryptContext


router = APIRouter()

BASE_DIR = Path(__file__).resolve().parent

templates = Jinja2Templates(directory="newapi/templates")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET = 'your-secret-key'
manager = LoginManager(SECRET, token_url='/auth/token')

 
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


@router.get("/registration/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("registration.html", {"request": request,})


@router.get("/login/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("login.html", {"request": request,})

@router.get("/log_success/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("loginsuccess.html", {"request": request,})

@router.get("/error/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("error.html", {"request": request,})

@router.get("/error1/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("error1.html", {"request": request,})


@router.post('/registration/',)
async def create_user(request: Request,email: str = Form(...),
                      name: str = Form(...), 
                      phone: str = Form(...),
                      password: str = Form(...)):
    if await newapi.filter(email=email).exists():
        return {"status":True,
                "message":"email already exists"}
        
    else:
        user_obj = await newapi.create(email=email,name=name,
                                     phone=phone
                                     ,password= get_password_hash(password))
        print(user_obj)                             
       
        return RedirectResponse("/login/", status_code=status.HTTP_302_FOUND)



@manager.user_loader()
async def load_user(email:str):
    if await newapi.exists(email=email):
        newapi1 = await newapi.get(email=email)
        return newapi1

@router.post('/user_login/', )
async def login(email:str = Form(...),
                password:str = Form(...)):
     
    
    email = email
    user = await load_user(email)
    
    if not user:
        return RedirectResponse("/error/", status_code=status.HTTP_302_FOUND)
        # return JSONResponse({'status':False,'message':'User not Registered'},status_code=403)
    elif not verify_password(password,user.password):
        return RedirectResponse("/error1/", status_code=status.HTTP_302_FOUND)

        # return JSONResponse({'status':False,'message':'Invalid password'},status_code=403)

    else:
        return RedirectResponse("/log_success/", status_code=status.HTTP_302_FOUND)