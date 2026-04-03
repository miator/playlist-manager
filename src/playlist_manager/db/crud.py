from typing import Optional

from sqlalchemy.orm import Session

from playlist_manager.db import models


def create_song(
    db: Session,
    title: str,
    artist: str,
    duration: int,
    genre: str,
    playlist_name: str,
):
    song = models.SongModel(
        title=title,
        artist=artist,
        duration=duration,
        genre=genre,
        playlist_name=playlist_name,
    )
    db.add(song)
    db.commit()
    db.refresh(song)
    return song


def get_song(db: Session, song_id: int):
    return db.query(models.SongModel).filter(models.SongModel.id == song_id).first()


def get_songs(db: Session, playlist_name: Optional[str] = None):
    query = db.query(models.SongModel)
    if playlist_name:
        query = query.filter(models.SongModel.playlist_name == playlist_name)
    return query.all()


def update_song(db: Session, song_id: int, **updates):
    song = get_song(db, song_id)
    if not song:
        return None

    for key, value in updates.items():
        if value is not None and hasattr(song, key):
            setattr(song, key, value)

    db.commit()
    db.refresh(song)
    return song


def delete_song(db: Session, song_id: int):
    song = get_song(db, song_id)
    if not song:
        return None

    db.delete(song)
    db.commit()
    return song
