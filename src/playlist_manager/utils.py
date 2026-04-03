from functools import wraps


def normalize_text(value: str, field_name: str) -> str:
    cleaned = value.strip()
    if not cleaned:
        raise ValueError(f"{field_name} cannot be empty")
    return cleaned


def parse_duration(value: str) -> int:
    cleaned = value.strip()
    if not cleaned:
        raise ValueError("Duration cannot be empty")

    if ":" in cleaned:
        parts = cleaned.split(":")
        if len(parts) != 2:
            raise ValueError("Duration must be in mm:ss format or total seconds")

        minutes, seconds = parts
        if not minutes.isdigit() or not seconds.isdigit():
            raise ValueError("Duration must contain only numbers")

        total_seconds = int(minutes) * 60 + int(seconds)
    else:
        if not cleaned.isdigit():
            raise ValueError("Duration must be a whole number of seconds")
        total_seconds = int(cleaned)

    if total_seconds <= 0:
        raise ValueError("Duration must be greater than 0")

    return total_seconds


def fmt_duration(seconds: int) -> str:
    minutes = seconds // 60
    remaining_seconds = seconds % 60
    return f"{minutes}:{remaining_seconds:02d}"


def ensure_playlist_exists(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        playlist_name = kwargs.get("playlist_name") or (args[0] if args else None)
        if not playlist_name:
            raise ValueError("Playlist name is required")
        if playlist_name not in self:
            raise KeyError(f"Playlist '{playlist_name}' does not exist")
        return func(self, *args, **kwargs)

    return wrapper
