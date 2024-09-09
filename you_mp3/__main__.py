"Module for using the tool via the command line"

from argparse import _ArgumentGroup as ArgumentGroup, ArgumentParser, Namespace

from os import remove
from os.path import isdir, splitext

from pathlib import Path

from typing import Any

from .downloader import Setting, download_music, extract_playlist
from .metadata import add_metadata, create_cover


def main() -> None:
    "Main function of the code"

    # Command line construction

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
        "-d --debug",
        help="enables runtime debugging",
        action="store_true",
        default=False,
        dest="debug"
    )

    arguments.add_argument(
        "-o",
        dest="output",
        help="location where the songs will be saved",
        type=str
    )

    group: ArgumentGroup = arguments.add_argument_group(
        title="editing",
        description="parameters for editing music"
    )

    group.add_argument(
        "-g",
        dest="genre",
        help="musical genres that will be attributed",
        default="Unknown Genre",
        type=str
    )


    # Argument handling

    args: Namespace = arguments.parse_args()

    url: str = args.url

    debug: bool = args.debug
    output: str | None = args.output

    genre: str = args.genre


    # Setting up YoutubeDL

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


    if type(output) == str:

        if isdir(output):
            config_download["outtmpl"] = f"{output}/%(title)s.%(ext)s"

        else:
            output = Path(output).stem
            config_download["outtmpl"] = output


    # Defining metadata

    data: dict[str, Any] = {"genre": genre}

    data_playlist: dict[str, Any] | None
    data_playlist = extract_playlist(url, config_extract)

    if data_playlist != None:

        track_total: int = len(data_playlist["musics"])
        data_playlist["track-total"] = str(track_total)

        track_number: int = 0

        for url in data_playlist["musics"]:

            track_number += 1

            data_playlist["track-number"] = str(track_number)
            data = {**data, **data_playlist}

            _download_handler(url, data, config_download)

    else:
        _download_handler(url, data, config_download)


def _download_handler(url: str, data: dict[str, Any], config: dict[str, Any]) -> None:
    """Internal music download function

    Args:
        url: link of the music that will be downloaded
        data: pre-extracted metadata that will be added to the music
        config: configuration dictionary that will be used in YoutubeDL
    """

    # Downloading music

    data_music: dict[str, str] | None
    data_music = download_music(url, config)

    if data_music != None:

        data = {**data, **data_music}

        path: str = data["path"]
        path, _ = splitext(path)

        image_path: str = f"{path}.webp"
        cover_path: str = create_cover(image_path)

        image: bytes = open(image_path, "rb").read()

        data["cover"] = image

        remove(image_path)
        remove(cover_path)

        add_metadata(f"{path}.mp3", data)


if __name__ == "__main__":
    main()
