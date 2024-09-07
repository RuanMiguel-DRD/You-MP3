"Module for downloading and extracting metadata from the platform"

from yt_dlp import YoutubeDL

from os import getcwd

from shutil import which

from typing import Any


_ERROR_TYPE: str = "Unexpected primitive type"
"Error if the data variable has a value with an incorrect primitive type"


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


def download_music(url: str, config: dict[str, Any] = Setting.DOWNLOAD) -> dict[str, str] | None:
    """Download the music and return your information

    Args:
        url: link to the music that will be downloaded
        config (optional): YoutubeDL configuration dictionary

    Returns:
        dict: dictionary with metadata about the downloaded music
        None: if it does not extract the metadata
    """

    if _ffmpeg_check(config):

        data: dict[str, str] | None
        with YoutubeDL(config) as youtube:
            data = youtube.extract_info(url, download=True)
            youtube.close()

        assert type(data) == dict, _ERROR_TYPE

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


def extract_playlist(url: str, config: dict[str, Any] = Setting.EXTRACT) -> dict[str, Any] | None:
    """Extract playlist information

    Args:
        url: playlist url from which the information will be extracted
        config (optional): dictionary containing settings for YoutubeDL.

    Returns:
        dict: dictionary containing structured information about the playlist
        None: if the url does not belong to a playlist
    """

    data: dict[str, str] | None
    with YoutubeDL(config) as youtube:
        data = youtube.extract_info(url, download=False)
        youtube.close()

    assert type(data) == dict, _ERROR_TYPE

    if "entries" in data:

        album: str = data.get("title", "Unknown Album")
        artist_album: str = data.get("uploader", "Unknown Artist Album")
        musics: list[str] = [entry.get("url") for entry in data["entries"]] # type: ignore

        return {
            "musics": musics,
            "album": album,
            "artist-album": artist_album
        }


def _ffmpeg_check(config: dict[str, Any]) -> bool:
    """Internal function to check if ffmpe_location is set correctly

    Args:
        config: YoutubeDL configuration dictionary

    Raises:
        KeyError: key \"ffmpeg_location\" is not defined in the dictionary
        TypeError: key \"ffmpeg_location\" is defined without a value

    Returns:
        bool: if it does not generate any error, it returns true
    """

    try:
        if config["ffmpeg_location"] != str:
            raise TypeError

        else:
            return True

    except (KeyError):
        raise KeyError("\"ffmpeg_location\" key not set")

    except (TypeError):
        raise TypeError("\"ffmpeg_location\" key set with invalid value")
