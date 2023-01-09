from tortoise.models import Model
from tortoise import Tortoise,fields
from fastapi import FastAPI
from tortoise import Tortoise




class newapi(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(200,)
    email = fields.CharField(200, unique=True)
    password =fields.CharField(200)
    phone = fields.CharField(10)


Tortoise.init_models(['newapi.models'],'models')