# Playlist Manager

A Python-based playlist management system with a command-line interface (CLI), FastAPI backend, and support for concurrency, database persistence, and external data loading from the iTunes API.

---

## **Features**

### 1. Playlist & Song Management
- Create multiple playlists.
- Add songs to playlists with **title, artist, duration, and genre**.
- Remove songs from playlists.
- View playlist contents with total songs and total duration.
- Navigate songs in playlists: **next** and **previous** simulation.

### 2. Search & Statistics
- Search songs across all playlists by **title** or **artist**.
- View statistics:
  - Total number of songs in the library.
  - Number of songs and total duration per playlist.

### 3. Data Persistence
- All playlists and songs are persisted in **SQLite database**.
- JSON backup is supported for offline storage.

### 4. Concurrency
- Load initial song data from iTunes API using:
  - **Threading** (I/O-bound tasks)
  - **Multiprocessing** (CPU-bound tasks, e.g., parsing/processing large datasets)

### 5. FastAPI Integration
- Provides a Python API to:
  - Create, read, update, delete songs.
  - Query playlists and search songs programmatically.

---