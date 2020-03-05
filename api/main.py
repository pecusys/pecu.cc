from fastapi import FastAPI, APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException
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
db = None
#------------APP-----------------------------#

app = FastAPI(
    title="pecu.cc",
    default_response_class=UJSONResponse,
)

@app.on_event('startup')
async def startup():
    if 'pecudb' not in client.list_database_names():
        db = client['pecudb']

#--------------AUTH-------------------------#

manager = LoginManager(SECRET, tokenUrl='/auth/token')

def load_user(email: str):
    user = db.users.get(email)
    return user


#--------------ROUTES---------------------#

@app.get("/")
def get_root():
    dbs = list()
    if len(client.list_database_names()) == 0:
        return {"DB status":"Not connected"}
    else:
        for d in client.list_database_names():
            dbs.append(str(d))
    return {"DB status":{"Connected!":dbs}}

@app.get("/dbtest")
def db_test():
    return {str(client.list_database_names())}

@app.post("/auth/token")
async def login(data: OAuth2PasswordRequestForm = Depends()):
    email = data.username
    password = data.password
    user = load_user(email)
    if not user or password != user['password']:
        raise InvalidCredentialsException

    access_token = manager.create_access_token(data=dict(sub=email))
    return {'access_token': access_token, 'token_type': 'bearer'}

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
        'method': 'chart.gettopartists'
    }
    r = requests.get(url, headers=headers, params=payload)
    return r.json()['artists']


def post_test():
    return {"Test":"test"}

@app.get("/dashboard")
async def get_dashboard(user=Depends(manager)):
    return {"Entries":{
        "Entry1":"1"
    }}
