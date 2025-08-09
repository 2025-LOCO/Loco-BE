from app.core.database import Base
from .user import User
from .region import Region
from .trip import Trip
from .loco import Loco
from .message import Message

# User 모델에 관계 추가
from sqlalchemy.orm import relationship

User.trips = relationship("Trip", back_populates="user")
User.loco_profile = relationship("Loco", back_populates="user", uselist=False)