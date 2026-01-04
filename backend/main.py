from fastapi import FastAPI
from api.drowsy import router

app = FastAPI()

@app.get("/")
def root():
    return {"status": "server running"}

app.include_router(router)