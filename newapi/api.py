from fastapi import FastAPI
from fastapi import APIRouter
from newapi.pydantic_models import createuser,loginuser,Token,updateuser,deleteuser
from . models import *


from fastapi.responses import JSONResponse
from fastapi_login import LoginManager
from fastapi.encoders import jsonable_encoder
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm

from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi import APIRouter,Request
from pathlib import Path 




router=APIRouter()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET = 'your-secret-key'
manager = LoginManager(SECRET, token_url='/auth/token')

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)



@router.post("/ragester/")
async def Create_user(data:createuser):
    if await newapi.filter(email=data.email).exists():
        return {"status":True,
                "message":"email already exists"}
    else:
       newapi_obj= await newapi.create(name=data.name,email=data.email,
                        phone=data.phone,password=get_password_hash(data.password))     

    return newapi_obj




@manager.user_loader()
async def load_user(email:str):
    if await newapi.exists(email=email):
        newapi1 = await newapi.get(email=email)
        return newapi1


@router.post('/login/', )
async def login(data:loginuser):
     
    
    email = data.email
    user = await load_user(email)
    
    if not user:
        return JSONResponse({'status':False,'message':'User not Registered'},status_code=403)
    elif not verify_password(data.password,user.password):
        return JSONResponse({'status':False,'message':'Invalid password'},status_code=403)
    access_token = manager.create_access_token(
        data={'sub':jsonable_encoder(user.email),"name":jsonable_encoder(user.email)}
    
    )
    '''test  current user'''
    
    
    new_dict = jsonable_encoder(user)
    new_dict.update({"access_token":access_token})
    return Token(access_token=access_token, token_type='bearer')

@router.put("/update/")
async def update_user(data:updateuser):
        if await newapi.exists(id =data.id):
                user_obj = await newapi.filter(id = data.id).update(name = data.name,email= data.email,password=data.password,phone = data.phone)
                print(user_obj)
                return {"Update user"}
        


@router.delete("/delete/")
async def delete_user(data: deleteuser):
    delete_user = await newapi.filter(email=data.user_email).delete()
    return  {"user delete successfully"}




@router.get("/index/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        })    



