from typing import List, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.region import Region
from app.schemas.region import RegionCreate, RegionBase

class CRUDRegion(CRUDBase[Region, RegionCreate, RegionBase]):
    def get_by_code(self, db: Session, *, code: str) -> Optional[Region]:
        return db.query(Region).filter(Region.code == code).first()

    def get_by_parent_code(self, db: Session, *, parent_code: str) -> List[Region]:
        return db.query(Region).filter(Region.parent_code == parent_code).all()

    def get_by_level(self, db: Session, *, level: int) -> List[Region]:
        return db.query(Region).filter(Region.level == level).all()

crud_region = CRUDRegion(Region)