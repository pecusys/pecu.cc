from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def read_root():
	return {"test":"try"}

app.m