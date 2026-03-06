from flask import Flask, render_template, request, jsonify
import sqlite3
import os

app = Flask(__name__)

# ---------------------------------
# DATABASE PATH
# ---------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "pyq.db")


# ---------------------------------
# DATABASE CONNECTION
# ---------------------------------

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# ---------------------------------
# HOME PAGE
# ---------------------------------

@app.route('/')
def index():

    conn = get_db()
    c = conn.cursor()

    c.execute("SELECT DISTINCT year FROM pyq_questions ORDER BY year")
    years = [row["year"] for row in c.fetchall()]

    conn.close()

    return render_template("index.html", years=years)


# ---------------------------------
# GET SUBJECTS
# ---------------------------------

@app.route('/get_subjects', methods=['POST'])
def get_subjects():

    year = request.form.get("year").strip()

    conn = get_db()
    c = conn.cursor()

    c.execute("""
        SELECT DISTINCT subject
        FROM pyq_questions
        WHERE LOWER(year) = LOWER(?)
        ORDER BY subject
    """, (year,))

    subjects = [row["subject"] for row in c.fetchall()]

    conn.close()

    return jsonify({"subjects": subjects})


# ---------------------------------
# GET UNITS
# ---------------------------------

@app.route('/get_units', methods=['POST'])
def get_units():

    year = request.form.get("year").strip()
    subject = request.form.get("subject").strip()

    conn = get_db()
    c = conn.cursor()

    c.execute("""
        SELECT DISTINCT unit
        FROM pyq_questions
        WHERE LOWER(year)=LOWER(?)
        AND LOWER(subject)=LOWER(?)
        ORDER BY unit
    """, (year, subject))

    units = [row["unit"] for row in c.fetchall()]

    conn.close()

    return jsonify({"units": units})


# ---------------------------------
# GET QUESTIONS
# ---------------------------------

@app.route('/questions', methods=['POST'])
def get_questions():

    year = request.form.get("year").strip()
    subject = request.form.get("subject").strip()
    unit = request.form.get("unit").strip()

    conn = get_db()
    c = conn.cursor()

    c.execute("""
        SELECT question_text, question_image, answer
        FROM pyq_questions
        WHERE LOWER(year)=LOWER(?)
        AND LOWER(subject)=LOWER(?)
        AND LOWER(unit)=LOWER(?)
        ORDER BY id
    """, (year, subject, unit))

    rows = c.fetchall()

    conn.close()

    questions = []

    for row in rows:

        image_path = row["question_image"]

        # ensure correct static path
        if image_path.startswith("static/"):
            image_path = image_path.replace("static/", "")

        questions.append({
            "text": row["question_text"],
            "image": image_path,
            "answer": row["answer"]
        })

    return render_template(
        "questions.html",
        questions=questions,
        year=year,
        subject=subject,
        unit=unit
    )


# ---------------------------------
# RUN SERVER
# ---------------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)