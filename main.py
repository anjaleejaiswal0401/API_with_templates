from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from newapi import api as newapiRoute
from newapi import routes as apiRoute
from fastapi.staticfiles import StaticFiles
from configs.connection import DATABASE_URL 
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware  



db_url = DATABASE_URL()
 
middleware = [
    Middleware(SessionMiddleware, secret_key='super-secret')
]
app = FastAPI(middleware=middleware)
app.mount('/static',StaticFiles(directory='static'))
app.include_router(newapiRoute.router, prefix="/newapi", tags=["newapi"]),
app.include_router(apiRoute.router,),


register_tortoise(
    app,
    db_url=db_url,
    modules={'models': ['newapi.models','aerich.models']},
    generate_schemas=True,
    add_exception_handlers=True
)