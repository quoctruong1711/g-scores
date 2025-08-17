from sqlalchemy import Column, Integer, String, Float, UniqueConstraint
from .database import Base

class StudentScore(Base):
    __tablename__ = "student_scores"

    id = Column(Integer, primary_key=True, index=True)
    sbd = Column(String, unique=True, index=True, nullable=False)  # Số báo danh

    # Các môn (nullable=True vì không phải ai cũng thi tất cả)
    toan = Column(Float, nullable=True)
    ngu_van = Column(Float, nullable=True)
    ngoai_ngu = Column(Float, nullable=True)
    vat_li = Column(Float, nullable=True)
    hoa_hoc = Column(Float, nullable=True)
    sinh_hoc = Column(Float, nullable=True)
    lich_su = Column(Float, nullable=True)
    dia_li = Column(Float, nullable=True)
    gdcd = Column(Float, nullable=True)
    ma_ngoai_ngu = Column(String, nullable=True)

    __table_args__ = (
        UniqueConstraint('sbd', name='uq_student_sbd'),
    )
