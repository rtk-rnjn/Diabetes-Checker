CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    gender VARCHAR(6) NOT NULL,
    age INTEGER NOT NULL,
    hypertension INT NOT NULL,
    heart_disease INT NOT NULL,
    smoking_history INT NOT NULL,
    bmi REAL NOT NULL,
    hb1ac_level REAL NOT NULL,
    blood_glucose_level REAL NOT NULL,
    diabetic INT NOT NULL
);