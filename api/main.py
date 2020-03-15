from fastapi import FastAPI, APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from fastapi_contrib.db.utils import setup_mongodb, create_indexes
from fastapi_contrib.db.models import MongoDBModel, MongoDBTimeStampedModel
from fastapi_contrib.common.responses import UJSONResponse
from fastapi_contrib.serializers import openapi
from fastapi_contrib.serializers.common import Serializer
# from pydantic import BaseModel
import pymongo
import requests
import json
import numpy as np

import api.config as cf

#-----------CONSTANTS-----------------------#

SECRET = cf.SECRET

#-----------MODELS--------------------------#
#@TODO IMPLEMENT MONGODB COLLECTIONS TO STORE ENTRIES

class User(MongoDBModel):
    _id: int
    username: str
    password: str
    class Meta:
        collection = "users"
        indexes = [pymongo.IndexModel('uid', name='_uid')]

class Entry(MongoDBTimeStampedModel):
    class Meta:

        collection = "entries"
        indexes = [pymongo.IndexModel('eid', name='_eid')]

#------------DB------------------------------#
# @TODO LINK DATABASE LOCAL TO FASTAPI INSTEAD OF MONGODB ATLAS

DEV_HOST = ('localhost', 27017)
ATLAS_HOST = cf.ATLAS_STRING
DBHOST = 'db.pecu.cc'

CLIENT = pymongo.MongoClient(ATLAS_HOST)
DB = CLIENT.pecudb
#------------APP-----------------------------#
app = FastAPI(
    title="pecu.cc",
    default_response_class=UJSONResponse,
)

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:3001"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event('startup')
async def startup():
    if 'pecudb' not in CLIENT.list_database_names():
        pass

#--------------AUTH-------------------------#


def load_user(email: str):
    user = DB.users.get(email)
    return user


#--------------ROUTES---------------------#

@app.get("/")
def get_root():
    dbs = list()
    if len(CLIENT.list_database_names()) == 0:
        return {"DB status":"Not connected"}
    for d in CLIENT.list_database_names():
        dbs.append(str(d))
    return {"DB status":{"Connected!":dbs}}

@app.get("/dbtest")
def db_test():
    return {str(CLIENT.list_database_names())}

@app.get('/items/{name}')
async def get_item(name: str):
    return {"name": name}

@app.get('/users/{username}')
async def get_user(username: str):
    return {'username': username}

@app.get("/lastfm/{user}")
async def get_lastfm(user: str):
    headers = {'user-agent': user}
    url = 'http://ws.audioscrobbler.com/2.0/'
    payload = {
        'api_key': cf.LASTFM_KEY,
        'format': 'json',
        'method': 'user.getTopArtists',
        'user': user,
        'period': '1month',
    }
    r = requests.get(url, headers=headers, params=payload)
    return r.json()

@app.get("/dashboard")
async def get_dashboard():
    return {"Entries":{
        "Entry1":"1"
    }}

@app.get("/test")
async def get_test():
    return
