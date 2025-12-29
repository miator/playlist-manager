from playlist_manager.core.manager import PlaylistManager
from playlist_manager.core.entities import Song
from playlist_manager.utils import parse_duration, fmt_duration
from playlist_manager.concurency.load_initial_data import load_initial_data


def main():
    with PlaylistManager('playlists.json') as manager:
        # Load initial iTunes songs if playlist does not exist
        if "Initial Playlist" not in manager:
            print("⏳ Loading initial playlist with iTunes songs...")
            load_initial_data(manager)
            print("✅ Initial playlist loaded!")

        print("\n--- Welcome to Your Playlist Manager ---")

        while True:
            print("\nMenu:")
            print("1) Create new playlist")
            print("2) Add song to playlist")
            print("3) View playlist")
            print("4) Play next song")
            print("5) Play previous song")
            print("6) Search songs")
            print("7) Save and Exit")

            choice = input("Choose an option [1-7]: ").strip()

            try:
                if choice == '1':
                    name = input("Enter playlist name: ").strip()
                    if not name:
                        raise ValueError("Playlist name cannot be empty")
                    manager.create_playlist(name)
                    print(f"✅ Playlist '{name}' created!")

                elif choice == '2':
                    if not manager:
                        print("No playlists exist. Create one first!")
                        continue
                    pname = input(f"Enter playlist name ({', '.join(manager.keys())}): ").strip()
                    if pname not in manager:
                        print(f"Playlist '{pname}' does not exist.")
                        continue
                    title = input("Song title: ").strip()
                    artist = input("Artist: ").strip()
                    duration_raw = input("Duration (mm:ss or seconds): ").strip()
                    genre = input("Genre: ").strip()

                    if not all([title, artist, duration_raw, genre]):
                        raise ValueError("All song details are required!")

                    duration = parse_duration(duration_raw)
                    song = Song(title, artist, duration, genre)
                    manager.add_song_to_playlist(pname, song)
                    print(f"🎵 Added '{song.title}' to '{pname}'")

                elif choice == '3':
                    if not manager:
                        print("No playlists exist.")
                        continue
                    pname = input(f"Enter playlist name ({', '.join(manager.keys())}): ").strip()
                    if pname not in manager:
                        print(f"Playlist '{pname}' does not exist.")
                        continue
                    playlist = manager[pname]
                    print(f"\nPlaylist '{pname}':")
                    for i, s in enumerate(playlist.list_songs(), start=1):
                        status = "<- NOW PLAYING" if i-1 == playlist._current_index else ""
                        print(f"{i}. {s.title} by {s.artist} [{fmt_duration(s.duration)}] ({s.genre}) {status}")
                    print(f"Total songs: {len(playlist)}, Total duration: {fmt_duration(playlist.total_duration())}")

                elif choice == '4':
                    pname = input(f"Enter playlist name ({', '.join(manager.keys())}): ").strip()
                    if pname in manager:
                        manager[pname].play_next()
                    else:
                        print("Playlist does not exist.")

                elif choice == '5':
                    pname = input(f"Enter playlist name ({', '.join(manager.keys())}): ").strip()
                    if pname in manager:
                        manager[pname].play_prev()
                    else:
                        print("Playlist does not exist.")

                elif choice == '6':
                    title = input("Search by title (optional): ").strip() or None
                    artist = input("Search by artist (optional): ").strip() or None
                    if not title and not artist:
                        print("Enter at least title or artist.")
                        continue
                    results = manager.search_all_playlists(title=title, artist=artist)
                    if not results:
                        print("No songs found.")
                        continue
                    for pname, songs in results.items():
                        print(f"\nFound in '{pname}':")
                        for s in songs:
                            print(f" - {s.title} by {s.artist} [{fmt_duration(s.duration)}] ({s.genre})")

                elif choice == '7':
                    manager.save()
                    print("💾 Library saved. Goodbye!")
                    break

                else:
                    print("Invalid option.")

            except Exception as e:
                print(f"Error: {e}")


if __name__ == "__main__":
    main()
