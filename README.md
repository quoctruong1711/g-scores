# Exam Score Lookup & Statistics System

## 📌 Introduction
This project consists of two parts:
- **Backend (FastAPI + SQLite/PostgreSQL/MySQL)**: provides APIs for statistics, top 10 rankings, and score lookup by exam ID (SBD).
- **Frontend (Plain HTML/CSS/JS)**: provides a user interface including:
  - Score distribution statistics per subject (with details for each Foreign Language code).
  - A table showing the Top 10 students with the highest total score in Block A (Math + Physics + Chemistry).
  - A score lookup form by SBD.

## ⚙️ Project Structure
```
g-scores/
│
├── backend/
│ ├── data
│ | └── diem_thi_thpt_2024.csv
│ ├── app
│ | ├── _init_.py 
│ | ├── main.py 
│ | ├── models.py 
│ | ├── database.py 
│ | ├── schemas.py 
│ | └──seed_csv.py 
│ ├── scores.db
│ └── requirements.txt
│
├── frontend/
│ ├── index.html 
│ ├── app.js
│ └── styles.css 
│
└── README.md
```

## 🚀 Run Backend (FastAPI)
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
2. Start the server:
   ```bash
   uvicorn main:app --reload
3. The backend will run at:
   👉 http://127.0.0.1:8000
   
You can test the API via Swagger UI:
👉 http://127.0.0.1:8000/docs

## 🌐 Run Frontend
1. Open frontend/index.html in your browser.
(You can also run with Live Server in VSCode or with Python: python -m http.server).
2. Main features:
- Statistics: click the "Show Statistics" button → displays subject score distributions.
- Top 10: automatically displays the Top 10 students in a table.
- Score Lookup: enter an SBD → view subject scores and Foreign Language code (if any).

📊 Main API Endpoints
- GET /stats → returns score distribution statistics by subject.
- GET /top10 → returns the Top 10 students.
- GET /score/{sbd} → lookup scores by SBD.

📝 Notes
- SBD values are stored as strings in the database.
- If an invalid SBD is entered → returns 404 with message Không tìm thấy SBD ("SBD not found").
- Foreign Language statistics are broken down by language code.
