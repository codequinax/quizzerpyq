import sqlite3
import os

# ---------------------------------
# PATH SETTINGS
# ---------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "pyq.db")
PYQ_FOLDER = os.path.join(BASE_DIR, "static", "pyq")

# ---------------------------------
# DATABASE CONNECTION
# ---------------------------------

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# ---------------------------------
# CREATE TABLE
# ---------------------------------

c.execute("""
CREATE TABLE IF NOT EXISTS pyq_questions (
id INTEGER PRIMARY KEY AUTOINCREMENT,
year TEXT,
subject TEXT,
unit TEXT,
question_text TEXT,
question_image TEXT UNIQUE,
answer TEXT
)
""")

# ---------------------------------
# INDEXES (FASTER FILTERING)
# ---------------------------------

c.execute("CREATE INDEX IF NOT EXISTS idx_year ON pyq_questions(year)")
c.execute("CREATE INDEX IF NOT EXISTS idx_subject ON pyq_questions(subject)")
c.execute("CREATE INDEX IF NOT EXISTS idx_unit ON pyq_questions(unit)")

# ---------------------------------
# SAFE NUMERIC SORT FUNCTION
# ---------------------------------

def sort_key(file):
    name = os.path.splitext(file)[0]
    if name.isdigit():
        return (0, int(name))
    return (1, name)

# ---------------------------------
# SCAN IMAGE FOLDERS
# ---------------------------------

records = []
total_images = 0

for year in sorted(os.listdir(PYQ_FOLDER)):

    year_path = os.path.join(PYQ_FOLDER, year)

    if not os.path.isdir(year_path):
        continue

    year_name = year.replace("_", " ").title()

    print(f"\n📂 Scanning {year_name}")

    for subject in sorted(os.listdir(year_path)):

        subject_path = os.path.join(year_path, subject)

        if not os.path.isdir(subject_path):
            continue

        print(f"   📘 Subject: {subject}")

        for unit in sorted(os.listdir(subject_path)):

            unit_path = os.path.join(subject_path, unit)

            if not os.path.isdir(unit_path):
                continue

            unit_name = unit.replace("_", " ").title()

            images = [
                f for f in os.listdir(unit_path)
                if f.lower().endswith((".png", ".jpg", ".jpeg", ".webp"))
            ]

            images.sort(key=sort_key)

            for file in images:

                image_path = f"pyq/{year}/{subject}/{unit}/{file}"

                records.append(
                    (
                        year_name,
                        subject,
                        unit_name,
                        "",
                        image_path,
                        ""
                    )
                )

                total_images += 1

# ---------------------------------
# INSERT DATA
# ---------------------------------

c.executemany("""
INSERT OR IGNORE INTO pyq_questions
(year, subject, unit, question_text, question_image, answer)
VALUES (?, ?, ?, ?, ?, ?)
""", records)

conn.commit()

# ---------------------------------
# SUMMARY
# ---------------------------------

count = c.execute("SELECT COUNT(*) FROM pyq_questions").fetchone()[0]

conn.close()

print("\n---------------------------------")
print(f"✅ Images scanned : {total_images}")
print(f"✅ Questions in DB: {count}")
print("---------------------------------")
