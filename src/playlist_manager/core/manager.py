import json
import os
from playlist_manager.core.entities import Playlist, Song
from playlist_manager.utils import ensure_playlist_exists


class PlaylistManager(dict):
    def __init__(self, filename='playlists.json'):
        super().__init__()
        self._filename = filename

    def __enter__(self):
        self.load()
        return self

    def __exit__(self, exc_type, exc, tb):
        self.save()
        return False

    def load(self):
        if not os.path.exists(self._filename):
            return
        try:
            with open(self._filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.clear()
            for pd in data.get('playlists', []):
                self[pd['name']] = Playlist.from_dict(pd)
        except Exception:
            print("Could not load playlists. Starting fresh.")

    def save(self):
        data = {'playlists': [p.to_dict() for p in self.values()]}
        with open(self._filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def create_playlist(self, name: str):
        if not name:
            raise ValueError("Playlist name cannot be empty")
        if name in self:
            raise KeyError(f"Playlist '{name}' exists")
        self[name] = Playlist(name)

    @ensure_playlist_exists
    def add_song_to_playlist(self, playlist_name: str, song: Song):
        self[playlist_name].add_song(song)

    @ensure_playlist_exists
    def remove_song_from_playlist(self, playlist_name: str, title: str, artist: str = None):
        self[playlist_name].remove_song(title, artist)

    @ensure_playlist_exists
    def list_playlist_songs(self, playlist_name: str):
        return self[playlist_name].list_songs()

    def search_all_playlists(self, title=None, artist=None):
        results = {}
        for pname, p in self.items():
            found = p.find(title, artist)
            if found:
                results[pname] = found
        return results

    def stats(self):
        total_songs = sum(len(p) for p in self.values())
        per_playlist = {pname: {'count': len(p), 'duration': p.total_duration()} for pname, p in self.items()}
        return {'total_songs': total_songs, 'per_playlist': per_playlist}
