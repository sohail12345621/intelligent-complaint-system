from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.database import init_db, insert_complaint, get_all_complaints, update_status, get_by_complaint_id
from app.classifier import predict_category
from app.priority import detect_priority
from app.models import ComplaintCreate, StatusUpdate
from app.auth import verify_admin

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
        row = insert_complaint(payload.text, category, priority)
    except Exception:
        raise HTTPException(status_code=500, detail="Database error while saving complaint")

    return {
        "id": row["id"],
        "complaint_id": row["complaint_id"],
        "category": row["category"],
        "priority": row["priority"],
        "status": row["status"]
    }

@app.get("/api/complaints")
def list_complaints(admin: str = Depends(verify_admin)):
    return get_all_complaints()

@app.put("/api/complaints/{complaint_id}/status")
def change_status(complaint_id: int, payload: StatusUpdate, admin: str = Depends(verify_admin)):
    success = update_status(complaint_id, payload.status)
    if not success:
        raise HTTPException(status_code=404, detail="Complaint not found")
    return {"id": complaint_id, "status": payload.status}

@app.get("/api/track/{complaint_id}")
def track_complaint(complaint_id: str):
    result = get_by_complaint_id(complaint_id.strip().upper())
    if not result:
        raise HTTPException(status_code=404, detail="No complaint found with that ID")
    return result

@app.get("/")
def home():
    return FileResponse("app/static/index.html")

@app.get("/track")
def track_page():
    return FileResponse("app/static/track.html")

@app.get("/admin")
def admin_page(admin: str = Depends(verify_admin)):
    return FileResponse("app/static/admin.html")

app.mount("/static", StaticFiles(directory="app/static"), name="static")
