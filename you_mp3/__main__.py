"Module for using the tool via the command line"

from argparse import _ArgumentGroup as ArgumentGroup, ArgumentParser, Namespace

from os import getcwd, mkdir, remove, rename

from typing import Any

from .downloader import Setting, download_music, extract_playlist
from .metadata import add_metadata, create_cover, trim_music

from .__utils import format_time


def main() -> None:
    "Main function of the code"

    arguments: ArgumentParser = ArgumentParser(
        prog="you-mp3",
        description="Program to download mp3 music directly from Youtube",
        epilog="https://github.com/RuanMiguel-DRD/You-MP3"
    )

    arguments.add_argument(
        "url",
        help="link to the song or playlist you want to download",
        type=str
    )

    arguments.add_argument(
        "-d", "--debug",
        dest="debug",
        help="enables runtime debugging",
        action="store_true",
        default=False
    )

    group_edition: ArgumentGroup = arguments.add_argument_group(
        title="edition",
        description="parameter for editing metadata"
    )

    group_edition.add_argument(
        "-g",
        dest="genre",
        help="musical genres that will be attributed",
        default="Unknown Genre",
        type=str
    )

    group_trim: ArgumentGroup = arguments.add_argument_group(
        title="trim",
        description="parameters for clipping songs, do not work with playlists"
    )

    group_trim.add_argument(
        "-s --start",
        dest="start",
        help="defines the moment the music should start",
        default="0"
    )

    group_trim.add_argument(
        "-e --end",
        dest="end",
        help="defines the moment the music should end",
        default="0"
    )

    args: Namespace = arguments.parse_args()

    url: str = args.url

    debug: bool = args.debug

    genre: str = args.genre
    start: str = args.start
    end: str = args.end

    config_download: dict[str, Any] = Setting.DOWNLOAD
    config_extract: dict[str, Any] = Setting.EXTRACT

    if debug == True:

        debug_config: dict[str, bool] = {
            "no_warnings": False,
            "logtostderr": False,
            "quiet": False
        }

        config_download.update(debug_config)
        config_extract.update(debug_config)

    data: dict[str, Any] = {"genre": genre}

    print("[you-mp3] Checking if the url belongs to a playlist")
    data.update(extract_playlist(url, config_extract))

    if data["playlist"] == True:

        album: str = data["album"]

        try:
            print(f"[you-mp3] Creating the album folder: {album}")
            mkdir(album)

        except (FileExistsError):
            ...

        config_download["outtmpl"] = f"{getcwd()}/{album}/%(title)s.%(ext)s"

    track_total: int = len(data["musics"])
    data["track-total"] = str(track_total)

    track_number: int = 0

    start_formatted: int = 0
    try:
        start_formatted = format_time(start)

    except (TypeError):
        print(f"[you-mp3] Invalid start time: {start}")

    end_formatted: int = 0
    try:
        end_formatted = format_time(end)

    except (TypeError):
        print(f"[you-mp3] Invalid end time: {end}")

    for music in data["musics"]:

        track_number += 1
        data["track-number"] = str(track_number)

        print(f"[you-mp3] Downloading the music: {music}")
        data.update(download_music(music, config_download))

        music_path: str = data["path"].replace(".webm", ".mp3")
        image_path: str = data["path"].replace(".webm", ".webp")

        cover_path: str = create_cover(image_path)
        image: bytes = open(image_path, "rb").read()

        data["cover"] = image

        if start_formatted != 0 or end_formatted != 0:

            try:
                trim_music_path: str = trim_music(music_path, start_formatted, end_formatted, debug)

                print(f"[you-mp3] Replacing original music: {music_path}")
                remove(music_path)
                rename(trim_music_path, music_path)

            except (ValueError) as err:
                print(f"[you-mp3] Unable to cut the music: {err}")

        print(f"[you-mp3] Removing pre-conversion files: \"{image_path}\" and \"{cover_path}\"")
        remove(image_path)
        remove(cover_path)

        print(f"[you-mp3] Adding metadata: {music_path}")
        add_metadata(music_path, data)


if __name__ == "__main__":
    main()
