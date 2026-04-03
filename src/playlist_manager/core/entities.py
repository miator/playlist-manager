from dataclasses import dataclass
from typing import Any, Optional

from playlist_manager.utils import fmt_duration, normalize_text


@dataclass
class Song:
    title: str
    artist: str
    duration: int
    genre: str

    def __post_init__(self) -> None:
        self.title = normalize_text(self.title, "Title")
        self.artist = normalize_text(self.artist, "Artist")
        self.genre = normalize_text(self.genre, "Genre")
        self.duration = int(self.duration)

        if self.duration <= 0:
            raise ValueError("Duration must be greater than 0")

    def __repr__(self) -> str:
        return (
            f"Song('{self.title}', '{self.artist}', "
            f"{fmt_duration(self.duration)}, '{self.genre}')"
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "artist": self.artist,
            "duration": self.duration,
            "genre": self.genre,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Song":
        return cls(
            title=data["title"],
            artist=data["artist"],
            duration=int(data["duration"]),
            genre=data["genre"],
        )


class Playlist:
    def __init__(self, name: str):
        self.name = normalize_text(name, "Playlist name")
        self._songs: list[Song] = []
        self._current_index = -1

    def __len__(self) -> int:
        return len(self._songs)

    def __repr__(self) -> str:
        return f"Playlist('{self.name}', {len(self)} songs)"

    @property
    def current_index(self) -> int:
        return self._current_index

    def add_song(self, song: Song) -> None:
        self._songs.append(song)
        if self._current_index == -1:
            self._current_index = 0

    def remove_song(self, title: str, artist: Optional[str] = None) -> None:
        normalized_title = normalize_text(title, "Song title")
        normalized_artist = artist.strip() if artist else None

        for index, song in enumerate(self._songs):
            title_matches = song.title == normalized_title
            artist_matches = normalized_artist is None or song.artist == normalized_artist
            if title_matches and artist_matches:
                del self._songs[index]
                if not self._songs:
                    self._current_index = -1
                elif self._current_index >= len(self._songs):
                    self._current_index = len(self._songs) - 1
                return

        raise KeyError(f"Song '{normalized_title}' not found")

    def list_songs(self) -> list[Song]:
        return list(self._songs)

    def play_next(self) -> Song:
        if not self._songs:
            raise ValueError("Playlist is empty")

        self._current_index = (self._current_index + 1) % len(self._songs)
        return self._songs[self._current_index]

    def play_prev(self) -> Song:
        if not self._songs:
            raise ValueError("Playlist is empty")

        self._current_index = (self._current_index - 1) % len(self._songs)
        return self._songs[self._current_index]

    def total_duration(self) -> int:
        return sum(song.duration for song in self._songs)

    def find(
        self,
        title: Optional[str] = None,
        artist: Optional[str] = None,
    ) -> list[Song]:
        title_query = title.strip().lower() if title else None
        artist_query = artist.strip().lower() if artist else None

        matches: list[Song] = []
        for song in self._songs:
            title_matches = title_query and title_query in song.title.lower()
            artist_matches = artist_query and artist_query in song.artist.lower()
            if title_matches or artist_matches:
                matches.append(song)
        return matches

    def to_dict(self) -> dict[str, Any]:
        return {"name": self.name, "songs": [song.to_dict() for song in self._songs]}

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Playlist":
        playlist = cls(data["name"])
        for song_data in data.get("songs", []):
            playlist.add_song(Song.from_dict(song_data))
        return playlist
