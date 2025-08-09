from typing import List, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.loco import Loco
from app.schemas.loco import LocoCreate, LocoUpdate

class CRUDLoco(CRUDBase[Loco, LocoCreate, LocoUpdate]):
    def get_by_user(self, db: Session, *, user_id: int) -> Optional[Loco]:
        return db.query(Loco).filter(Loco.user_id == user_id).first()

    def get_by_region(self, db: Session, *, region_id: int) -> List[Loco]:
        return db.query(Loco).filter(
            Loco.region_id == region_id,
            Loco.is_available == True
        ).all()

    def create_with_user(self, db: Session, *, obj_in: LocoCreate, user_id: int) -> Loco:
        db_obj = Loco(**obj_in.dict(), user_id=user_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

crud_loco = CRUDLoco(Loco)