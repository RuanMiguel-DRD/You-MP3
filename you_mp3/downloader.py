"Module for downloading and extracting metadata from the platform"

from yt_dlp import YoutubeDL

from os import getcwd

from shutil import which

from typing import Any

from .__utils import ERROR_TYPE, ffmpeg_check


class Setting():
    "Class containing predefined settings for use in YoutubeDL"

    BASE: dict[str, bool] = {
        "force_generic_extractor": False,
        "no_warnings": True,
        "logtostderr": True,
        "quiet": True,
        "debug": False
    }
    "Configuration dictionary base"

    EXTRACT: dict[str, bool] = {
        "extract_flat": True,
        "skip_download": True,
        **BASE
    }
    "Configuration dictionary for playlist extraction"

    DOWNLOAD: dict[str, Any] = {
        "skip_download": False,
        "overwrites": True,
        "noplaylist": True,
        "writethumbnail": True,
        "extract_audio": True,
        "format": "bestaudio/best",
        "ffmpeg_location": which("ffmpeg"),
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "0",
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
        config (optional): YoutubeDL configuration dictionary

    Returns:
        dict: dictionary with metadata about the downloaded music
    """

    ffmpeg_check(config)

    data: dict[str, str] | None
    with YoutubeDL(config) as youtube:
        data = youtube.extract_info(url)
        youtube.close()

    assert type(data) == dict, ERROR_TYPE

    path: str = youtube.prepare_filename(data)
    title: str = data.get("title", "Unknown Title")
    artist: str = data.get("uploader", "Unknown Artist")
    date: str = data.get("upload_date", "Unknown Date")
    date = f"{date[:4]}-{date[4:6]}-{date[6:]}"

    return {
        "path": path,
        "title": title,
        "artist": artist,
        "date": date
    }


def extract_playlist(url: str, config: dict[str, Any] = Setting.EXTRACT) -> dict[str, Any]:
    """Extract playlist information

    Args:
        url: playlist url from which the information will be extracted
        config (optional): dictionary containing settings for YoutubeDL.

    Returns:
        dict: dictionary containing structured information about the playlist
    """

    data: dict[str, str] | None
    with YoutubeDL(config) as youtube:
        data = youtube.extract_info(url)
        youtube.close()

    assert type(data) == dict, ERROR_TYPE

    if "entries" in data:

        album: str = data.get("title", "Unknown Album")
        artist_album: str = data.get("uploader", "Unknown Artist Album")
        musics: list[str] = [entry.get("url") for entry in data["entries"]] # type: ignore

        return {
            "playlist": True,
            "musics": musics,
            "album": album,
            "artist-album": artist_album
        }

    else:
        return {
            "playlist": False,
            "musics": [url]
        }
