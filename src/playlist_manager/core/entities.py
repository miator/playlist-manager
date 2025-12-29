from typing import Dict, Any
from playlist_manager.utils import fmt_duration


class Entity:
    def __init__(self, name: str):
        if not name:
            raise ValueError("Name cannot be empty")
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if not value:
            raise ValueError("Name cannot be empty")
        self._name = value


class Song(Entity):
    def __init__(self, title: str, artist: str, duration: int, genre: str):
        super().__init__(title)
        self.artist = artist
        self.duration = duration
        self.genre = genre

    @property
    def title(self): return self.name

    @title.setter
    def title(self, value): self.name = value

    @property
    def artist(self): return self._artist

    @artist.setter
    def artist(self, value):
        if not value:
            raise ValueError("Artist cannot be empty")
        self._artist = value

    @property
    def duration(self): return self._duration

    @duration.setter
    def duration(self, value):
        if value < 0:
            raise ValueError("Duration cannot be negative")
        self._duration = int(value)

    @property
    def genre(self): return self._genre

    @genre.setter
    def genre(self, value):
        if not value:
            raise ValueError("Genre cannot be empty")
        self._genre = value

    def __repr__(self):
        return f"Song('{self.title}', '{self.artist}', {fmt_duration(self.duration)}, '{self.genre}')"

    def __eq__(self, other):
        return isinstance(other, Song) and self.title == other.title and self.artist == other.artist

    def to_dict(self) -> Dict[str, Any]:
        return {'title': self.title, 'artist': self.artist, 'duration': self.duration, 'genre': self.genre}

    @classmethod
    def from_dict(cls, d: Dict[str, Any]):
        return cls(d['title'], d['artist'], int(d['duration']), d['genre'])


class Playlist(Entity):
    def __init__(self, name: str):
        super().__init__(name)
        self._songs: list[Song] = []
        self._current_index: int = -1

    def __len__(self):
        return len(self._songs)

    def __repr__(self):
        return f"Playlist('{self.name}', {len(self)} songs)"

    def __eq__(self, other):
        return isinstance(other, Playlist) and self.name == other.name and self._songs == other._songs

    def add_song(self, song: Song):
        self._songs.append(song)
        if self._current_index == -1:
            self._current_index = 0

    def remove_song(self, title: str, artist: str = None):
        for i, s in enumerate(self._songs):
            if s.title == title and (artist is None or s.artist == artist):
                del self._songs[i]
                if not self._songs:
                    self._current_index = -1
                elif self._current_index >= len(self._songs):
                    self._current_index = len(self._songs) - 1
                return
        raise KeyError(f"Song '{title}' not found.")

    def list_songs(self):
        return list(self._songs)

    def play_next(self):
        if not self._songs:
            print("Playlist is empty")
            return
        self._current_index = (self._current_index + 1) % len(self._songs)
        song = self._songs[self._current_index]
        print(f"Now playing: {song.title} by {song.artist} [{fmt_duration(song.duration)}]")

    def play_prev(self):
        if not self._songs:
            print("Playlist is empty")
            return
        self._current_index = (self._current_index - 1) % len(self._songs)
        song = self._songs[self._current_index]
        print(f"Now playing: {song.title} by {song.artist} [{fmt_duration(song.duration)}]")

    def total_duration(self):
        return sum(s.duration for s in self._songs)

    def find(self, title=None, artist=None):
        res = []
        for s in self._songs:
            if (title and title.lower() in s.title.lower()) or (artist and artist.lower() in s.artist.lower()):
                res.append(s)
        return res

    def to_dict(self):
        return {'name': self.name, 'songs': [s.to_dict() for s in self._songs]}

    @classmethod
    def from_dict(cls, d):
        p = cls(d['name'])
        for sdict in d.get('songs', []):
            p.add_song(Song.from_dict(sdict))
        return p
