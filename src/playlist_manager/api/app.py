from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from playlist_manager.db import crud, database, models

models.Base.metadata.create_all(bind=database.engine)
app = FastAPI(title="Playlist Manager API")


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/songs/")
def add_song(title: str, artist: str, duration: int, genre: str, playlist_id: int, db: Session = Depends(get_db)):
    return crud.create_song(db, title, artist, duration, genre, playlist_id)


@app.get("/songs/{song_id}")
def read_song(song_id: int, db: Session = Depends(get_db)):
    song = crud.get_song(db, song_id)
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")
    return song


@app.get("/songs/")
def list_songs(playlist_id: int = None, db: Session = Depends(get_db)):
    return crud.get_songs(db, playlist_id)


@app.put("/songs/{song_id}")
def edit_song(song_id: int, title: str = None, artist: str = None, duration: int = None, genre: str = None,
              db: Session = Depends(get_db)):
    song = crud.update_song(db, song_id, title=title, artist=artist, duration=duration, genre=genre)
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")
    return song


@app.delete("/songs/{song_id}")
def remove_song(song_id: int, db: Session = Depends(get_db)):
    song = crud.delete_song(db, song_id)
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")
    return {"detail": "Song deleted"}
