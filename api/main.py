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

#-----------CONSTANTS-----------------------#
SECRET = "test_key"

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
prod_host = 'db.pecu.cc'

client = pymongo.MongoClient(dev_host[0], dev_host[1])
db = client['pecudb']
users = db['users']

#------------APP-----------------------------#

app = FastAPI(
    title="pecu.cc",
    default_response_class=UJSONResponse,
)

@app.on_event('startup')
async def startup():
    setup_mongodb(app)
    await create_indexes()

#--------------AUTH-------------------------#

manager = LoginManager(SECRET, tokenUrl='/auth/token')

def load_user(email: str):
    user = db.get(email)
    return user

@manager

#--------------ROUTES---------------------#

@app.get("/")
def get_root():
    return {"Test":{"Thing":"Thing2"}}

@app.post("/auth/token")
async def login(data: OAuth2PasswordRequestForm = Depends()):
    email = data.username
    password = data.password
    user = load_user(email)
    if not user or password != user['password']:
        raise InvalidCredentialsException

@app.get("/test")
def get_test():
    return {"Test"}

def post_test():
    return {"Test":"test"}

@app.get("/dashboard")
async def get_dashboard(user=Depends(manager)):
    return {"Entries":{
        "Entry1":"1"
    }}
