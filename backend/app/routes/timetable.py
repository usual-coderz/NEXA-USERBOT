from fastapi import APIRouter
from app.services.generator import generate_schedule

router = APIRouter(prefix="/timetable")

@router.post("/generate")
def generate(data: dict):
    tasks = data.get("tasks", [])
    start_time = data.get("start", 0)

    schedule = generate_schedule(tasks, start_time)
    return {"schedule": schedule}