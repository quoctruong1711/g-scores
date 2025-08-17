from pydantic import BaseModel
from typing import Optional

class ScoreOut(BaseModel):
    sbd: str
    toan: Optional[float] = None
    ngu_van: Optional[float] = None
    ngoai_ngu: Optional[float] = None
    vat_li: Optional[float] = None
    hoa_hoc: Optional[float] = None
    sinh_hoc: Optional[float] = None
    lich_su: Optional[float] = None
    dia_li: Optional[float] = None
    gdcd: Optional[float] = None
    ma_ngoai_ngu: Optional[str] = None

    class Config:
        from_attributes = True  # Pydantic v2
