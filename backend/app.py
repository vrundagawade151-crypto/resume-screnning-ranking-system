from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import traceback

from database import get_connection
from resume_parser import extract_text
from scoring import calculate_score

# ---------------- SETUP ----------------
app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "../uploads/resumes"
FRONTEND_FOLDER = "../frontend"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# ---------------- FRONTEND ROUTES ----------------
@app.route("/")
def home_page():
    return send_from_directory(FRONTEND_FOLDER, "index.html")

@app.route("/recruiter")
def recruiter_page():
    return send_from_directory(FRONTEND_FOLDER, "recruiter.html")

@app.route("/candidate")
def candidate_page():
    return send_from_directory(FRONTEND_FOLDER, "candidate.html")

# Serve CSS/JS files
@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory(FRONTEND_FOLDER, filename)


# ---------------- JOB UPLOAD ----------------
@app.route("/upload_job", methods=["POST"])
def upload_job():
    try:
        title = request.form["title"]
        skills = request.form["skills"]
        exp = request.form.get("experience")
        edu = request.form.get("education")

        conn = get_connection()
        cur = conn.cursor()

        sql = "INSERT INTO jobs(title,skills,experience,education) VALUES(%s,%s,%s,%s)"
        cur.execute(sql, (title, skills, exp, edu))

        conn.commit()
        conn.close()

        return jsonify({"msg": "Job Posted Successfully"})

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


# ---------------- RESUME UPLOAD ----------------
@app.route("/upload_resume", methods=["POST"])
def upload_resume():
    try:
        name = request.form["name"]
        file = request.files["resume"]

        ext = file.filename.split(".")[-1].lower()
        if ext not in ["pdf","docx"]:
            return jsonify({"msg":"Invalid File Format"}),400

        path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(path)

        text = extract_text(path)

        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT skills FROM jobs ORDER BY id DESC LIMIT 1")
        job = cur.fetchone()
        if not job:
            return jsonify({"msg":"No Job Available"}),400

        job_skills = job[0]
        score = calculate_score(text, job_skills)
        status = "Shortlisted" if score >= 30 else "Rejected"

        sql = "INSERT INTO resumes(name,file,text,score,status) VALUES(%s,%s,%s,%s,%s)"
        cur.execute(sql, (name,file.filename,text,score,status))

        conn.commit()
        conn.close()

        return jsonify({"msg":"Resume Uploaded","score":score,"status":status})

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


# ---------------- VIEW RESULTS ----------------
@app.route("/results", methods=["GET"])
def results():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT name,score,status FROM resumes ORDER BY score DESC")
        rows = cur.fetchall()
        conn.close()

        data = [{"name": r[0], "score": r[1], "status": r[2]} for r in rows]
        return jsonify(data)

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


# ---------------- RUN SERVER ----------------
if __name__ == "__main__":
    app.run(debug=True)
