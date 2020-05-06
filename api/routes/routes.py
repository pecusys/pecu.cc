from fastapi import FastAPI, APIRouter

router = APIRouter()

@router.get("/test?q=?")
def test_route():
    return {"FD":"DSF"}

