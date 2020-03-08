from fastapi import FastAPI, APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_contrib.db.utils import setup_mongodb, create_indexes
from fastapi_contrib.db.models import MongoDBModel, MongoDBTimeStampedModel
from fastapi_contrib.common.responses import UJSONResponse
from fastapi_contrib.serializers import openapi
from fastapi_contrib.serializers.common import Serializer
from pydantic import BaseModel
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
dev_host = ('localhost', 27017)
atlas_host = cf.ATLAS_STRING
prod_host = 'db.pecu.cc'

client = pymongo.MongoClient(atlas_host)
db = client.pecudb
#------------APP-----------------------------#

app = FastAPI(
    title="pecu.cc",
    default_response_class=UJSONResponse,
)

@app.on_event('startup')
async def startup():
    if 'pecudb' not in client.list_database_names():
        pass

#--------------AUTH-------------------------#


def load_user(email: str):
    user = db.users.get(email)
    return user


#--------------ROUTES---------------------#

@app.get("/")
def get_root():
    dbs = list()
    if len(client.list_database_names()) == 0:
        return {"DB status":"Not connected"}
    for d in client.list_database_names():
        dbs.append(str(d))
    return {"DB status":{"Connected!":dbs}}

@app.get("/dbtest")
def db_test():
    return {str(client.list_database_names())}

@app.get("/test")
def get_test():
    return {"Test"}

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
