from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, Enum, ForeignKey, UniqueConstraint
from app.core.database import Base
from app.models.vote_enums import VoteType

class PlaceVote(Base):
    __tablename__ = "place_votes"
    __table_args__ = (
        UniqueConstraint("user_id", "place_id", name="uq_place_vote_user_place"),
    )

    place_vote_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    place_id: Mapped[int] = mapped_column(ForeignKey("places.place_id"), index=True)
    vote_type: Mapped[VoteType] = mapped_column(Enum(VoteType), nullable=False)

    user = relationship("User", back_populates="place_votes")
    place = relationship("Place", back_populates="votes")


class RouteVote(Base):
    __tablename__ = "route_votes"
    __table_args__ = (
        UniqueConstraint("user_id", "route_id", name="uq_route_vote_user_route"),
    )

    route_vote_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    route_id: Mapped[int] = mapped_column(ForeignKey("routes.route_id"), index=True)
    vote_type: Mapped[VoteType] = mapped_column(Enum(VoteType), nullable=False)

    user = relationship("User", back_populates="route_votes")
    route = relationship("Route", back_populates="votes")