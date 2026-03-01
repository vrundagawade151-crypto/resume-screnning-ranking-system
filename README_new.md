# AI Resume Screening Starter

## Stack
- Frontend: React (Vite)
- Backend: Flask API

## Project Structure
- `frontend/` React app
- `backend/` Flask server
- `uploads/resumes/` Uploaded files

## Run Backend (Flask)
1. `cd backend`
2. `python -m venv venv`
3. `venv\\Scripts\\activate`
4. `pip install -r requirements.txt`
5. `python app.py`

Backend runs on `http://127.0.0.1:5000`

## Run Frontend (React)
1. Open a new terminal
2. `cd frontend`
3. `npm install`
4. `npm run dev`

Frontend runs on `http://127.0.0.1:5173`

## Available API Endpoints
- `GET /api/health`
- `GET /api/jobs`
- `POST /api/jobs`
- `POST /api/apply`
- `GET /api/applicants`

## Notes
- Current storage is in-memory for jobs/applications (resets on backend restart).
- Resume upload accepts `.pdf` and `.docx`.
- React UI now includes Home, Candidate, and Recruiter pages with routing.
