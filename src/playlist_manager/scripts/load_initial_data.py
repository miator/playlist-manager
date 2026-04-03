from concurrent.futures import ThreadPoolExecutor, as_completed

import requests

from playlist_manager.core.entities import Song
from playlist_manager.core.manager import PlaylistManager

ITUNES_SEARCH_URL = "https://itunes.apple.com/search"
DEFAULT_GENRES = ("pop", "rock", "jazz", "hip hop")


def fetch_songs_from_itunes(term: str, limit: int = 10) -> list[Song]:
    response = requests.get(
        ITUNES_SEARCH_URL,
        params={"term": term, "entity": "song", "limit": limit},
        timeout=10,
    )
    response.raise_for_status()

    songs: list[Song] = []
    for item in response.json().get("results", []):
        songs.append(
            Song(
                title=item.get("trackName", "Unknown Title"),
                artist=item.get("artistName", "Unknown Artist"),
                duration=item.get("trackTimeMillis", 180000) // 1000,
                genre=item.get("primaryGenreName", term.title()),
            )
        )
    return songs


def load_initial_data(
    manager: PlaylistManager,
    playlist_name: str = "Initial Playlist",
) -> None:
    if playlist_name not in manager:
        manager.create_playlist(playlist_name)

    with ThreadPoolExecutor(max_workers=len(DEFAULT_GENRES)) as executor:
        futures = {
            executor.submit(fetch_songs_from_itunes, genre): genre
            for genre in DEFAULT_GENRES
        }

        for future in as_completed(futures):
            genre = futures[future]
            try:
                songs = future.result()
            except requests.RequestException as exc:
                print(f"Could not load songs for '{genre}': {exc}")
                continue

            for song in songs:
                manager.add_song_to_playlist(playlist_name, song)
