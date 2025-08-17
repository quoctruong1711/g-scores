from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import Base, engine, get_db
from .models import StudentScore
from .schemas import ScoreOut
from typing import Dict, List
from sqlalchemy import func

app = FastAPI(title="G-Scores (FastAPI)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Cho phép mọi domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Tạo bảng khi khởi động lần đầu
Base.metadata.create_all(bind=engine)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/score/{sbd}", response_model=ScoreOut)
def get_score_by_sbd(sbd: str, db: Session = Depends(get_db)):
    student = db.query(StudentScore).filter(StudentScore.sbd == sbd).first()
    if not student:
        raise HTTPException(status_code=404, detail="Không tìm thấy SBD")
    return student


@app.get("/stats")
def get_stats(db: Session = Depends(get_db)) -> Dict[str, Dict]:
    subjects = [
        "toan", "ngu_van", "vat_li",
        "hoa_hoc", "sinh_hoc", "lich_su", "dia_li", "gdcd"
    ]
    result: Dict[str, Dict] = {}

    # Thống kê cho các môn thông thường
    for subj in subjects:
        col = getattr(StudentScore, subj)
        result[subj] = {
            ">=8": db.query(func.count()).filter(col >= 8).scalar(),
            "6-8": db.query(func.count()).filter(col >= 6, col < 8).scalar(),
            "4-6": db.query(func.count()).filter(col >= 4, col < 6).scalar(),
            "<4": db.query(func.count()).filter(col < 4).scalar(),
        }

    # Thống kê cho môn Ngoại ngữ, tách theo ma_ngoai_ngu
    result["ngoai_ngu"] = {}
    langs = db.query(StudentScore.ma_ngoai_ngu).distinct().all()
    for (lang_code,) in langs:
        col = StudentScore.ngoai_ngu
        result["ngoai_ngu"][lang_code] = {
            ">=8": db.query(func.count()).filter(col >= 8, StudentScore.ma_ngoai_ngu == lang_code).scalar(),
            "6-8": db.query(func.count()).filter(col >= 6, col < 8, StudentScore.ma_ngoai_ngu == lang_code).scalar(),
            "4-6": db.query(func.count()).filter(col >= 4, col < 6, StudentScore.ma_ngoai_ngu == lang_code).scalar(),
            "<4": db.query(func.count()).filter(col < 4, StudentScore.ma_ngoai_ngu == lang_code).scalar(),
        }

    return result


@app.get("/top10", response_model=List[ScoreOut])
def get_top10_groupA(db: Session = Depends(get_db)):
    students = (
        db.query(StudentScore)
        .filter(StudentScore.toan != None,
                StudentScore.vat_li != None,
                StudentScore.hoa_hoc != None)
        .all()
    )

    students_sorted = sorted(
        students,
        key=lambda s: (s.toan or 0) + (s.vat_li or 0) + (s.hoa_hoc or 0),
        reverse=True
    )

    return students_sorted[:10]
