"Module for using the tool via the command line"

from argparse import ArgumentParser, Namespace

from os import remove
from os.path import exists, splitext

from typing import Any

from .downloader import Setting, download_music, extract_playlist
from .metadata import add_metadata, create_cover


def _download_handler(url: str, data: dict[str, Any], config: dict[str, Any]) -> None:
    """Internal music download function

    Args:
        url: link of the music that will be downloaded
        data: pre-extracted metadata that will be added to the music
        config: configuration dictionary that will be used in YoutubeDL
    """

    # Downloading music

    data_music: dict[str, str] = download_music(url, config)

    data = {**data, **data_music}

    path: str = data["path"]
    path, _ = splitext(path)

    image_path: str = create_cover(f"{path}.webp")
    image: bytes = open(image_path, "rb").read()

    data["cover"] = image

    remove(image_path)

    add_metadata(f"{path}.mp3", data)


def main() -> None:
    "Main function of the code"

    # Command line construction

    arguments: ArgumentParser = ArgumentParser(
        prog="you-mp3",
        description="Program to download mp3 music directly from Youtube",
        epilog="https://github.com/RuanMiguel-DRD/You-MP3",
    )

    arguments.add_argument(
        "url",
        help="link to the song or playlist you want to download",
        type=str
    )

    arguments.add_argument(
        "-g",
        dest="genre",
        help="musical genres that will be attributed to the music",
        type=str
    )

    arguments.add_argument(
        "-o",
        dest="output",
        help="location where the songs will be saved",
        type=str
    )

    arguments.add_argument(
        "-q",
        dest="quality",
        default="medium",
        choices=["low", "medium", "high"],
        help="choose the sound quality level",
        type=str
    )

    # Argument handling

    args: Namespace = arguments.parse_args()

    url: str = args.url

    genre: str | None = args.genre if args.genre != None else "Unknown Genre"
    output: str | None = args.output
    quality: str = args.quality

    match quality:
        case "low": quality = "128"
        case "medium": quality = "192"
        case "high": quality = "320"

    # Setting up YoutubeDL

    config: dict[str, Any] = Setting.DOWNLOAD

    config["postprocessors"][0]["preferredquality"] = quality

    if type(output) == str:

        if exists(output):
            config["outtmpl"] = f"{output}/%(title)s.%(ext)s"

        else:
            config["outtmpl"] = output

    # Defining metadata

    data: dict[str, Any] = {"genre": genre}

    data_playlist: dict[str, Any]

    data_playlist = extract_playlist(url)

    if data_playlist["playlist"] == True:

        track_total: int = len(data_playlist["musics"])
        data_playlist["track-total"] = str(track_total)

        track_number: int = 0

        for url in data_playlist["musics"]:

            track_number += 1

            data_playlist["track-number"] = str(track_number)
            data = {**data, **data_playlist}

            _download_handler(url, data, config)

    else:
        _download_handler(url, data, config)


if __name__ == "__main__":
    main()
