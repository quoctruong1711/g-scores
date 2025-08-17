import sys
from pathlib import Path
import pandas as pd
from sqlalchemy.orm import Session
from unidecode import unidecode

from .database import Base, engine, SessionLocal
from .models import StudentScore

# Các tên cột chấp nhận cho từng môn
COLUMN_ALIASES = {
    "sbd": ["sbd", "so_bao_danh", "so bao danh"],
    "toan": ["toan", "math", "m"],
    "ngu_van": ["ngu_van", "nguvan", "van", "literature"],
    "ngoai_ngu": ["ngoai_ngu", "ngoaingu", "anh", "tieng_anh", "english"],
    "vat_li": ["vat_li", "vatli", "ly", "physics"],
    "hoa_hoc": ["hoa_hoc", "hoahoc", "hoa", "chemistry"],
    "sinh_hoc": ["sinh_hoc", "sinhhoc", "sinh", "biology"],
    "lich_su": ["lich_su", "lichsu", "su", "history"],
    "dia_li": ["dia_li", "diali", "dia", "geography"],
    "gdcd": ["gdcd", "giao_duc_cong_dan", "giaoduccongdan", "civics"],
    "ma_ngoai_ngu":["ma_ngoai_ngu", "mangoaingu", "ma_nn", "language_code"]
}

def _norm(s: str) -> str:
    """Chuẩn hóa tên cột: bỏ dấu, lower, thay khoảng trắng bằng '_'."""
    s = unidecode(str(s)).lower().strip()
    s = s.replace(" ", "_")
    s = s.replace("-", "_")
    return s

def guess_column(df: pd.DataFrame, logical_name: str):
    """Tìm cột trong df tương ứng với logical_name theo alias."""
    candidates = [ _norm(c) for c in df.columns ]
    alias = [ _norm(a) for a in COLUMN_ALIASES.get(logical_name, []) ]
    for i, c in enumerate(candidates):
        if c in alias:
            return df.columns[i]
    return None

def to_float(val):
    if pd.isna(val):
        return None
    s = str(val).strip()
    if s == "" or s == "-":
        return None
    # đổi , -> . cho số thập phân kiểu VN
    s = s.replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return None

def read_csv_any_encoding(path: Path) -> pd.DataFrame:
    # thử nhiều encoding và sep
    for enc in ["utf-8", "utf-8-sig", "cp1258", "latin-1"]:
        try:
            return pd.read_csv(path, dtype=str, encoding=enc, engine="python", sep=None)
        except Exception:
            continue
    # fallback: để pandas tự đoán
    return pd.read_csv(path, dtype=str, engine="python")

def import_csv(csv_path: str):
    csv_file = Path(csv_path)
    if not csv_file.exists():
        raise FileNotFoundError(f"Không thấy file: {csv_file.resolve()}")

    print(f"[INFO] Đang đọc CSV: {csv_file}")
    df = read_csv_any_encoding(csv_file)

    # Tìm các cột cần thiết
    colmap = {}
    required = ["sbd"]
    optional_subjects = ["toan","ngu_van","ngoai_ngu","vat_li","hoa_hoc","sinh_hoc","lich_su","dia_li","gdcd","ma_ngoai_ngu"]

    for name in required + optional_subjects:
        actual = guess_column(df, name)
        colmap[name] = actual

    if colmap["sbd"] is None:
        raise RuntimeError("Không tìm thấy cột SBD trong CSV. Hãy kiểm tra header.")

    # Khởi tạo DB
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()

    try:
        # Xóa dữ liệu cũ (nếu muốn làm sạch)
        # db.query(StudentScore).delete()
        # db.commit()

        records = []
        for _, row in df.iterrows():
            sbd = str(row[colmap["sbd"]]).strip() if row.get(colmap["sbd"]) is not None else None
            if not sbd:
                continue

            data = dict(sbd=sbd)
            for subj in optional_subjects:
                col = colmap.get(subj)
                if col is None:
                    data[subj] = None
                elif subj == "ma_ngoai_ngu":
                    # giữ dạng string
                    data[subj] = str(row[col]).strip() if pd.notna(row[col]) else None
                else:
                    data[subj] = to_float(row[col])

            records.append(StudentScore(**data))

        print(f"[INFO] Số bản ghi sẽ insert: {len(records)}")
        # Chia batch để tránh quá nặng
        BATCH = 1000
        for i in range(0, len(records), BATCH):
            db.add_all(records[i:i+BATCH])
            db.commit()
            print(f"  -> Đã commit {min(i+BATCH, len(records))}/{len(records)}")

        print("[DONE] Import CSV hoàn tất.")
    finally:
        db.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Cách dùng: python -m backend.app.seed_csv backend/data/diem_thi_thpt_2024.csv")
        sys.exit(1)
    import_csv(sys.argv[1])
