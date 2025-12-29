import requests
import threading
import multiprocessing
from playlist_manager.core.manager import PlaylistManager
from playlist_manager.core.entities import Song


def fetch_songs_from_itunes(term: str, limit_songs: int = 10):
    """
    Fetch songs from iTunes API for a given genre/term.
    Returns a list of Song objects.
    """
    url = f"https://itunes.apple.com/search?term={term}&entity=song&limit={limit_songs}"
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json().get("results", [])

    songs = []
    for d in data:
        duration_sec = d.get("trackTimeMillis", 180000) // 1000  # default 3 minutes
        song = Song(
            title=d.get("trackName", "Unknown Title"),
            artist=d.get("artistName", "Unknown Artist"),
            duration=duration_sec,
            genre=d.get("primaryGenreName", term)
        )
        songs.append(song)
    return songs


def load_songs_thread(manager: PlaylistManager, playlist_name: str, term: str):
    """I/O-bound task: fetch songs for one genre and add to playlist"""
    songs = fetch_songs_from_itunes(term=term, limit_songs=10)
    for s in songs:
        manager.add_song_to_playlist(playlist_name, s)


def compute_heavy_task(n: int):
    """CPU-bound task example using multiprocessing"""
    total = sum(i * i for i in range(1, n))
    return total


def load_initial_data(manager: PlaylistManager):
    """Load initial playlist with multiple genres concurrently"""
    playlist_name = "Initial Playlist"
    if playlist_name not in manager:
        manager.create_playlist(playlist_name)

    genres = ["pop", "rock", "jazz", "hip hop"]
    threads = []

    # Create and start threads for each genre
    for genre in genres:
        t = threading.Thread(target=load_songs_thread, args=(manager, playlist_name, genre))
        threads.append(t)
        t.start()

    # CPU-bound task example
    process = multiprocessing.Process(target=compute_heavy_task, args=(100_000,))
    process.start()

    # Wait for all threads to finish
    for t in threads:
        t.join()

    # Wait for CPU-bound process to finish
    process.join()
