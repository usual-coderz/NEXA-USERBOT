from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import timetable

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(timetable.router)

@app.get("/")
def root():
    return {"message": "StudyFlow API running"}