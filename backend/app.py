from flask import Flask, request, jsonify
from flask_cors import CORS

import os

from database import get_connection
from resume_parser import extract_text
from scoring import calculate_score


# ---------------- SETUP ----------------

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "../uploads/resumes"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# ---------------- JOB UPLOAD ----------------

@app.route("/upload_job", methods=["POST"])
def upload_job():

    title = request.form["title"]
    skills = request.form["skills"]
    exp = request.form["experience"]
    edu = request.form["education"]

    conn = get_connection()
    cur = conn.cursor()

    sql = """
    INSERT INTO jobs(title,skills,experience,education)
    VALUES(%s,%s,%s,%s)
    """

    cur.execute(sql, (title,skills,exp,edu))

    conn.commit()
    conn.close()

    return jsonify({"msg":"Job Posted Successfully"})


# ---------------- RESUME UPLOAD ----------------

@app.route("/upload_resume", methods=["POST"])
def upload_resume():

    name = request.form["name"]
    file = request.files["resume"]

    ext = file.filename.split(".")[-1].lower()

    if ext not in ["pdf","docx"]:
        return jsonify({"msg":"Invalid File Format"}),400


    path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(path)


    # Extract resume text
    text = extract_text(path)


    conn = get_connection()
    cur = conn.cursor()


    # Get latest job
    cur.execute("SELECT skills FROM jobs ORDER BY id DESC LIMIT 1")

    job = cur.fetchone()

    if not job:
        return jsonify({"msg":"No Job Available"}),400


    job_skills = job[0]


    # Calculate score
    score = calculate_score(text, job_skills)


    # Status
    status = "Rejected"

    if score >= 30:
        status = "Shortlisted"


    # Save resume
    sql = """
    INSERT INTO resumes(name,file,text,score,status)
    VALUES(%s,%s,%s,%s,%s)
    """

    cur.execute(sql, (name,file.filename,text,score,status))

    conn.commit()
    conn.close()


    return jsonify({
        "msg":"Resume Uploaded",
        "score":score,
        "status":status
    })


# ---------------- VIEW RESULTS ----------------

@app.route("/results", methods=["GET"])
def results():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    SELECT name,score,status
    FROM resumes
    ORDER BY score DESC
    """)

    rows = cur.fetchall()

    conn.close()


    data = []

    for r in rows:
        data.append({
            "name":r[0],
            "score":r[1],
            "status":r[2]
        })


    return jsonify(data)


# ---------------- RUN SERVER ----------------

if __name__ == "__main__":
    app.run(debug=True)
