from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.database import init_db, insert_complaint, get_all_complaints, update_status
from app.classifier import predict_category
from app.priority import detect_priority
from app.models import ComplaintCreate, StatusUpdate

app = FastAPI(title="Intelligent Complaint Classification System")

init_db()

@app.post("/api/complaints")
def create_complaint(payload: ComplaintCreate):
    try:
        category = predict_category(payload.text)
    except FileNotFoundError as e:
        raise HTTPException(status_code=503, detail=str(e))

    priority = detect_priority(payload.text)

    try:
        new_id = insert_complaint(payload.text, category, priority)
    except Exception:
        raise HTTPException(status_code=500, detail="Database error while saving complaint")

    return {"id": new_id, "category": category, "priority": priority, "status": "Pending"}

@app.get("/api/complaints")
def list_complaints():
    return get_all_complaints()

@app.put("/api/complaints/{complaint_id}/status")
def change_status(complaint_id: int, payload: StatusUpdate):
    success = update_status(complaint_id, payload.status)
    if not success:
        raise HTTPException(status_code=404, detail="Complaint not found")
    return {"id": complaint_id, "status": payload.status}

@app.get("/")
def home():
    return FileResponse("app/static/index.html")

@app.get("/admin")
def admin():
    return FileResponse("app/static/admin.html")

app.mount("/static", StaticFiles(directory="app/static"), name="static")
