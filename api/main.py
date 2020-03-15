from fastapi import FastAPI, APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_contrib.db.utils import setup_mongodb, create_indexes
from fastapi_contrib.db.models import MongoDBModel, MongoDBTimeStampedModel
from fastapi_contrib.common.responses import UJSONResponse
from fastapi_contrib.serializers import openapi
from fastapi_contrib.serializers.common import Serializer
# from pydantic import BaseModel
import pymongo
import requests
import json

import api.config as cf
#-----------CONSTANTS-----------------------#
SECRET = cf.SECRET

#-----------MODELS--------------------------#
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


def post_test():
    return {"Test":"test"}

@app.get("/dashboard")
async def get_dashboard():
    return {"Entries":{
        "Entry1":"1"
    }}

@app.get("/test")
async def get_test():
    return
