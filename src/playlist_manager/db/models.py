from sqlalchemy import Column, Integer, String
from playlist_manager.db.database import Base


class SongModel(Base):
    __tablename__ = "songs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    artist = Column(String, nullable=False)
    duration = Column(Integer, nullable=False)
    genre = Column(String, nullable=False)
    playlist_name = Column(String, nullable=False)  # matches CRUD
