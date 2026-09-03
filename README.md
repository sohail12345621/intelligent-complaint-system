# Intelligent Complaint Classification & Priority Detection System

## Installation
```
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Train the model
```
python ml/train_model.py
```

## Run locally
```
uvicorn app.main:app --reload
```
Visit http://127.0.0.1:8000 (user) and http://127.0.0.1:8000/admin (admin).

## Testing
Submit a complaint like "There has been no electricity in my hostel room since yesterday." → expect Category: Electricity, Priority: HIGH.

## GitHub upload
```
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-repo-url>
git push -u origin main
```

## Free deployment (Render)
1. Push repo to GitHub.
2. On Render.com → New Web Service → connect repo.
3. Build command: `pip install -r requirements.txt && python ml/train_model.py`
4. Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Free tier note: filesystem is ephemeral — SQLite data resets on redeploy/restart. Acceptable for a college demo.

## Sample complaints for demo
- "There has been no electricity in my hostel room since yesterday." → Electricity / HIGH
- "Wifi is not working in my hostel room." → Internet / MEDIUM
- "Suggestion to extend library working hours." → Other / LOW
- "Medical emergency in hostel, need immediate help." → Security / HIGH

## Viva explanation
- **TF-IDF**: converts complaint text into weighted word-frequency vectors, giving rarer/more meaningful words higher importance.
- **Logistic Regression**: a fast, interpretable linear classifier suited to small text datasets like this.
- **Priority**: rule-based keyword matching (HIGH > MEDIUM > LOW) — simple, transparent, easy to explain/defend in viva.
- **FastAPI**: modern, async Python framework with automatic docs (`/docs`), ideal for small REST APIs.
- **SQLite**: zero-config, file-based database — no server setup needed for a small project.
- **Deployment**: Render Free tier hosts the FastAPI app directly from GitHub at no cost.

## Future scalability
```
SQLite         → PostgreSQL
Local ML model → Model microservice
Single instance → Multiple instances behind load balancer
Small dataset  → Larger, real-world labeled dataset
```
