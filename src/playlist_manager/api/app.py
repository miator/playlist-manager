from typing import Generator, Optional

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from playlist_manager.api.schemas import SongCreate, SongRead, SongUpdate
from playlist_manager.db import crud, database, models

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Playlist Manager API")


def get_db() -> Generator[Session, None, None]:
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/songs/", response_model=SongRead)
def add_song(payload: SongCreate, db: Session = Depends(get_db)):
    return crud.create_song(db, **payload.model_dump())


@app.get("/songs/{song_id}", response_model=SongRead)
def read_song(song_id: int, db: Session = Depends(get_db)):
    song = crud.get_song(db, song_id)
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")
    return song


@app.get("/songs/", response_model=list[SongRead])
def list_songs(
    playlist_name: Optional[str] = None,
    db: Session = Depends(get_db),
):
    return crud.get_songs(db, playlist_name)


@app.put("/songs/{song_id}", response_model=SongRead)
def edit_song(song_id: int, payload: SongUpdate, db: Session = Depends(get_db)):
    song = crud.update_song(db, song_id, **payload.model_dump(exclude_none=True))
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")
    return song


@app.delete("/songs/{song_id}")
def remove_song(song_id: int, db: Session = Depends(get_db)):
    song = crud.delete_song(db, song_id)
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")
    return {"detail": "Song deleted"}
