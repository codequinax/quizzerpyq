from flask import Flask, render_template, request, jsonify, url_for
import sqlite3
import os

app = Flask(**name**)

# ---------------------------------

# DATABASE PATH

# ---------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(**file**))
DB_PATH = os.path.join(BASE_DIR, "pyq.db")

# ---------------------------------

# SUBJECT & UNIT MAP

# ---------------------------------

subject_map = {
'1st Year': ['Maths', 'Physics', 'PPS', 'Electrical', 'Mechanical', 'Chemistry', 'Workshop', 'English', 'Graphics', 'EVS'],
'2nd Year': ['DBMS', 'OS', 'DSA', 'CN', 'Maths', 'Software Engg', 'COA', 'OOPs', 'AI', 'ML'],
'3rd Year': ['BCAI051', 'Compiler', 'DAA', 'Web Tech', 'Cloud', 'Big Data', 'IOT', 'Python', 'Mobile Dev', 'Security'],
'4th Year': ['Project', 'Seminar', 'Internship', 'Management', 'Ethics', 'BlockChain', 'DevOps', 'Deep Learning', 'AR/VR', 'Robotics']
}

unit_map = {
subject: [f'Unit {i}' for i in range(1, 6)]
for subjects in subject_map.values()
for subject in subjects
}

# ---------------------------------

# HOME

# ---------------------------------

@app.route('/')
def index():
years = list(subject_map.keys())
return render_template('index.html', years=years)

# ---------------------------------

# GET SUBJECTS

# ---------------------------------

@app.route('/get_subjects', methods=['POST'])
def get_subjects():
year = request.form.get('year')
subjects = subject_map.get(year, [])
return jsonify({'subjects': subjects})

# ---------------------------------

# GET UNITS

# ---------------------------------

@app.route('/get_units', methods=['POST'])
def get_units():
subject = request.form.get('subject')
units = unit_map.get(subject, [])
return jsonify({'units': units})

# ---------------------------------

# GET QUESTIONS

# ---------------------------------

@app.route('/questions', methods=['POST'])
def get_questions():

```
year = request.form['year']
subject = request.form['subject']
unit = request.form['unit']

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
c = conn.cursor()

c.execute("""
    SELECT question_text, question_image, answer
    FROM pyq_questions
    WHERE year=? AND subject=? AND unit=?
""", (year, subject, unit))

rows = c.fetchall()
conn.close()

questions = []

for row in rows:

    image_path = row['question_image']

    if image_path:
        image_path = url_for('static', filename=image_path)

    questions.append({
        'text': row['question_text'],
        'image': image_path,
        'answer': row['answer']
    })

return render_template(
    'questions.html',
    questions=questions,
    year=year,
    subject=subject,
    unit=unit
)
```

# ---------------------------------

# RUN

# ---------------------------------

if **name** == "**main**":
app.run(host="0.0.0.0", port=5000, debug=True)
