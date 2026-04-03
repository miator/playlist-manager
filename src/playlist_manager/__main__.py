from typing import Optional

from playlist_manager.scripts.load_initial_data import load_initial_data
from playlist_manager.core.entities import Song
from playlist_manager.core.manager import PlaylistManager
from playlist_manager.utils import fmt_duration, parse_duration


def get_default_playlist_name(manager: PlaylistManager) -> Optional[str]:
    if not manager:
        return None
    return next(iter(manager))


def prompt_for_existing_playlist(manager: PlaylistManager) -> Optional[str]:
    if not manager:
        print("No playlists exist. Create one first.")
        return None

    playlist_name = input(f"Enter playlist name ({', '.join(manager.keys())}): ").strip()
    if playlist_name not in manager:
        print(f"Playlist '{playlist_name}' does not exist.")
        return None

    return playlist_name


def print_playlist(playlist_name: str, manager: PlaylistManager) -> None:
    playlist = manager[playlist_name]
    print(f"\nPlaylist '{playlist_name}':")

    for index, song in enumerate(playlist.list_songs(), start=1):
        status = " <- now playing" if index - 1 == playlist.current_index else ""
        print(
            f"{index}. {song.title} by {song.artist} "
            f"[{fmt_duration(song.duration)}] ({song.genre}){status}"
        )

    print(
        f"Total songs: {len(playlist)}, "
        f"total duration: {fmt_duration(playlist.total_duration())}"
    )


def print_current_song(song: Song) -> None:
    print(f"Now playing: {song.title} by {song.artist} [{fmt_duration(song.duration)}]")


def main() -> None:
    with PlaylistManager("../playlists.json") as manager:
        if "Initial Playlist" not in manager:
            print("Loading initial playlist with iTunes songs...")
            load_initial_data(manager)
            print("Initial playlist loaded.")

        active_playlist_name = get_default_playlist_name(manager)

        print("\nPlaylist Manager")

        while True:
            print("\nMenu:")
            print("1) Create new playlist")
            print("2) Add song to playlist")
            print("3) View playlist")
            print("4) Play next song")
            print("5) Play previous song")
            print("6) Search songs")
            print("7) Save and exit")

            choice = input("Choose an option [1-7]: ").strip()

            try:
                if choice == "1":
                    name = input("Enter playlist name: ").strip()
                    manager.create_playlist(name)
                    active_playlist_name = name
                    print(f"Playlist '{name}' created.")

                elif choice == "2":
                    playlist_name = prompt_for_existing_playlist(manager)
                    if not playlist_name:
                        continue

                    active_playlist_name = playlist_name
                    title = input("Song title: ").strip()
                    artist = input("Artist: ").strip()
                    duration_raw = input("Duration (mm:ss or seconds): ").strip()
                    genre = input("Genre: ").strip()

                    song = Song(
                        title=title,
                        artist=artist,
                        duration=parse_duration(duration_raw),
                        genre=genre,
                    )
                    manager.add_song_to_playlist(playlist_name, song)
                    print(f"Added '{song.title}' to '{playlist_name}'.")

                elif choice == "3":
                    playlist_name = prompt_for_existing_playlist(manager)
                    if playlist_name:
                        active_playlist_name = playlist_name
                        print_playlist(playlist_name, manager)

                elif choice == "4":
                    if not active_playlist_name:
                        print("No playlist selected yet.")
                        continue
                    print_current_song(manager[active_playlist_name].play_next())

                elif choice == "5":
                    if not active_playlist_name:
                        print("No playlist selected yet.")
                        continue
                    print_current_song(manager[active_playlist_name].play_prev())

                elif choice == "6":
                    title = input("Search by title (optional): ").strip() or None
                    artist = input("Search by artist (optional): ").strip() or None
                    if not title and not artist:
                        print("Enter at least a title or artist.")
                        continue

                    results = manager.search_all_playlists(title=title, artist=artist)
                    if not results:
                        print("No songs found.")
                        continue

                    for playlist_name, songs in results.items():
                        print(f"\nFound in '{playlist_name}':")
                        for song in songs:
                            print(
                                f"- {song.title} by {song.artist} "
                                f"[{fmt_duration(song.duration)}] ({song.genre})"
                            )

                elif choice == "7":
                    manager.save()
                    print("Library saved. Goodbye.")
                    break

                else:
                    print("Invalid option.")

            except (KeyError, ValueError) as exc:
                print(f"Error: {exc}")


if __name__ == "__main__":
    main()
