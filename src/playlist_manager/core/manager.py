import json
from pathlib import Path
from typing import Optional

from playlist_manager.core.entities import Playlist, Song
from playlist_manager.utils import ensure_playlist_exists, normalize_text


class PlaylistManager(dict):
    def __init__(self, filename: str = "playlists.json"):
        super().__init__()
        self._file_path = Path(filename)

    def __enter__(self) -> "PlaylistManager":
        self.load()
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:
        self.save()
        return False

    def load(self) -> None:
        if not self._file_path.exists():
            return

        try:
            with self._file_path.open("r", encoding="utf-8") as file:
                data = json.load(file)
        except (json.JSONDecodeError, OSError):
            print("Could not load playlists. Starting with an empty library.")
            return

        self.clear()
        for playlist_data in data.get("playlists", []):
            playlist = Playlist.from_dict(playlist_data)
            self[playlist.name] = playlist

    def save(self) -> None:
        data = {"playlists": [playlist.to_dict() for playlist in self.values()]}
        with self._file_path.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=2, ensure_ascii=False)

    def create_playlist(self, name: str) -> Playlist:
        normalized_name = normalize_text(name, "Playlist name")
        if normalized_name in self:
            raise KeyError(f"Playlist '{normalized_name}' already exists")

        playlist = Playlist(normalized_name)
        self[normalized_name] = playlist
        return playlist

    @ensure_playlist_exists
    def add_song_to_playlist(self, playlist_name: str, song: Song) -> None:
        self[playlist_name].add_song(song)

    @ensure_playlist_exists
    def remove_song_from_playlist(
        self,
        playlist_name: str,
        title: str,
        artist: Optional[str] = None,
    ) -> None:
        self[playlist_name].remove_song(title, artist)

    @ensure_playlist_exists
    def list_playlist_songs(self, playlist_name: str) -> list[Song]:
        return self[playlist_name].list_songs()

    def search_all_playlists(
        self,
        title: Optional[str] = None,
        artist: Optional[str] = None,
    ) -> dict[str, list[Song]]:
        results: dict[str, list[Song]] = {}
        for playlist_name, playlist in self.items():
            matches = playlist.find(title=title, artist=artist)
            if matches:
                results[playlist_name] = matches
        return results

    def stats(self) -> dict[str, object]:
        total_songs = sum(len(playlist) for playlist in self.values())
        per_playlist = {
            playlist_name: {
                "count": len(playlist),
                "duration": playlist.total_duration(),
            }
            for playlist_name, playlist in self.items()
        }
        return {"total_songs": total_songs, "per_playlist": per_playlist}
