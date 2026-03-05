import sqlite3
import os

# ---------------------------------

# DATABASE PATH

# ---------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "pyq.db")

# ---------------------------------

# CREATE DATABASE

# ---------------------------------

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# Drop table if exists

c.execute("DROP TABLE IF EXISTS pyq_questions")

# Create table

c.execute("""
CREATE TABLE pyq_questions (
id INTEGER PRIMARY KEY AUTOINCREMENT,
year TEXT,
subject TEXT,
unit TEXT,
question_text TEXT,
question_image TEXT,
answer TEXT
)
""")

# ---------------------------------

# SAMPLE DATA

# ---------------------------------

sample_data = [
('1st Year', 'Maths', 'Unit 1', '', '', '216 and 1'),
('1st Year', 'Maths', 'Unit 1', '', '', 'linearly dependent'),
('2nd Year', 'DBMS', 'Unit 2', 'Define primary key and foreign key.', '', 'Primary key uniquely identifies a row; foreign key links two tables.'),

('3rd Year', 'BCAI051', 'Unit 1', '', 'pyq/3rd_year/BCAI051/unit_1/1.png', ''),
('3rd Year', 'BCAI051', 'Unit 1', '', 'pyq/3rd_year/BCAI051/unit_1/2.png', ''),
('3rd Year', 'BCAI051', 'Unit 1', '', 'pyq/3rd_year/BCAI051/unit_1/3.png', ''),
('3rd Year', 'BCAI051', 'Unit 2', '', 'pyq/3rd_year/BCAI051/unit_2/1.png', ''),
('3rd Year', 'BCAI051', 'Unit 3', '', 'pyq/3rd_year/BCAI051/unit_3/1.png', '')

]

# ---------------------------------

# INSERT DATA

# ---------------------------------

c.executemany("""
INSERT INTO pyq_questions (year, subject, unit, question_text, question_image, answer)
VALUES (?, ?, ?, ?, ?, ?)
""", sample_data)

conn.commit()
conn.close()

print("✅ Database created successfully with sample data")
