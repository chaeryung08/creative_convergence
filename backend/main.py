from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.drowsy import router as drowsy_router
from api.alarm import router as alarm_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"status": "server running"}

app.include_router(drowsy_router)
app.include_router(alarm_router)