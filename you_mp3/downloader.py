"Module for downloading and extracting metadata from the platform"

from yt_dlp import YoutubeDL

from os import getcwd
from os.path import exists

from shutil import which

from typing import Any


_ERROR_TYPE: str = "Unexpected primitive type"
"Error if the data variable has a value with an incorrect primitive type"

_ERROR_FFMPEG: str = "Invalid path to ffmpeg"
"Error if ffmpeg_location is defined with an invalid path"


class Setting():
    "Class containing predefined settings for use in YoutubeDL"

    BASE: dict[str, bool] = {
        "force_generic_extractor": False,
        "no_warnings": True,
        "logtostderr": True,
        "quiet": True
    }
    "Configuration dictionary base"

    EXTRACT: dict[str, bool] = {
        "extract_flat": True,
        **BASE
    }
    "Configuration dictionary for playlist extraction"

    DOWNLOAD: dict[str, Any] = {
        "noplaylist": True, # Prevents the entire playlist from downloading automatically
        "writethumbnail": True,
        "extract_audio": True,
        "format": "bestaudio/best",
        "ffmpeg_location": which("ffmpeg"), # Set the path to the ffmpeg executable if the function returns None
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "outtmpl": f"{getcwd()}/%(title)s.%(ext)s",
        **BASE
    }
    "Configuration dictionary for music download"


def download_music(url: str, config: dict[str, Any] = Setting.DOWNLOAD) -> dict[str, str]:
    """Download the music and return your information

    Args:
        url: link to the music that will be downloaded
        config (optional): dictionary containing settings for YoutubeDL

    Returns:
        metadata: dictionary with metadata about the downloaded music
    """

    try:
        if "ffmpeg_location" in config:
            if not exists(config["ffmpeg_location"]):
                raise TypeError

    except (TypeError):
        raise TypeError(_ERROR_FFMPEG)

    data: dict[str, str] | None
    with YoutubeDL(config) as youtube:
        data = youtube.extract_info(url, download=True)
        youtube.close()

    if type(data) != dict:
        raise TypeError(_ERROR_TYPE)

    path: str = youtube.prepare_filename(data)
    title: str = data.get("title", "Unknown Title")
    artist: str = data.get("uploader", "Unknown Artist")
    date: str = data.get("upload_date", "Unknown Date")
    date = f"{date[:4]}-{date[4:6]}-{date[6:]}"

    metadata: dict[str, str] = {
        "path": path,
        "title": title,
        "artist": artist,
        "date": date
    }

    return metadata


def extract_playlist(url: str, config: dict[str, Any] = Setting.EXTRACT) -> dict[str, Any]:
    """Extract playlist information

    Args:
        url: playlist url from which the information will be extracted
        config (optional): dictionary containing settings for YoutubeDL.

    Returns:
        metadata: dictionary containing structured information about the playlist
    """

    data: dict[str, str] | None
    with YoutubeDL(config) as youtube:
        data = youtube.extract_info(url, download=False)
        youtube.close()

    if type(data) != dict:
        raise TypeError(_ERROR_TYPE)

    metadata: dict[str, Any] = {}

    if "entries" in data:

        album: str = data.get("title", "Unknown Album")
        artist_album: str = data.get("uploader", "Unknown Artist Album")
        musics: list[str] = [entry.get("url") for entry in data["entries"]] # type: ignore

        metadata = {
            "playlist": True,
            "musics": musics,
            "album": album,
            "artist-album": artist_album
        }

        return metadata

    else:

        metadata = {
            "playlist": False
        }

        return metadata
