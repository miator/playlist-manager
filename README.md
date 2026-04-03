# Playlist Manager

Playlist Manager is a small Python project for creating and managing playlists through a command-line interface and a simple FastAPI backend. It stores playlist data in JSON for the CLI flow and includes a separate SQLite-backed API for song records.

## What It Does

- Create playlists from the CLI
- Add songs with title, artist, duration, and genre
- Browse playlist contents and total duration
- Move to the next or previous song in a playlist
- Search songs across all playlists
- Load starter songs from the iTunes Search API
- Manage songs through a small FastAPI CRUD API

## Project Structure

```text
src/
  playlist_manager/
    api/            # FastAPI app and request/response schemas
    concurrency/    # iTunes loading with threaded requests
    core/           # playlist and song domain logic
    db/             # SQLAlchemy database setup and CRUD helpers
    __main__.py     # CLI entry point
    utils.py        # shared parsing and validation helpers
```

## Tech Stack

- Python 3.9+
- FastAPI
- SQLAlchemy
- Requests
- SQLite

## Installation

```bash
git clone https://github.com/miator/playlist-manager.git
cd playlist-manager
python -m venv .venv
.venv\Scripts\activate
pip install -e .
```

## Run The CLI

```bash
python -m playlist_manager
```

The CLI saves playlist data to `playlists.json` in the project root.

## Run The API

```bash
uvicorn playlist_manager.api.app:app --reload
```

The API creates `playlist.db` in the project root on first run.

## Example API Endpoints

- `POST /songs/` to create a song
- `GET /songs/` to list all songs or filter by `playlist_name`
- `GET /songs/{song_id}` to fetch one song
- `PUT /songs/{song_id}` to update a song
- `DELETE /songs/{song_id}` to delete a song

Example create request:

```json
{
  "title": "Numb",
  "artist": "Linkin Park",
  "duration": 185,
  "genre": "Rock",
  "playlist_name": "Favorites"
}
```

## Notes

- The CLI and API are intentionally small and straightforward.
- The iTunes loader uses threading because the work is network-bound.
- The project is meant to demonstrate clean Python structure, persistence, API basics, and external API integration without turning into a large production system.
