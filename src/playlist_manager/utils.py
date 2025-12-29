from functools import wraps


def parse_duration(s: str) -> int:
    s = s.strip()
    if ":" in s:
        parts = s.split(":")
        minutes = int(parts[0])
        seconds = int(parts[1])
        return minutes * 60 + seconds
    return int(s)


def fmt_duration(sec: int) -> str:
    m = sec // 60
    s = sec % 60
    return f"{m}:{s:02d}"


def ensure_playlist_exists(func):
    """Decorator to ensure playlist exists before performing action."""
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        playlist_name = kwargs.get('playlist_name') or (args[0] if args else None)
        if not playlist_name:
            raise ValueError("Playlist name is required.")
        if playlist_name not in self:
            raise KeyError(f"Playlist '{playlist_name}' does not exist.")
        return func(self, *args, **kwargs)
    return wrapper
