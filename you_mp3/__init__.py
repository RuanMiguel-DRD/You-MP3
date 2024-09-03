"""Library for downloading music and adding metadata
The library is an automation and abstraction layer of YoutubeDL
It can be used via the command line with the command \"you-mp3\""""

# Library information

__description__ = "Library for downloading music and adding metadata"

__status__ = "Educational"
__license__ = "Unlicense"
__version__ = "1.0.0"

__author__ = "RuanMiguel-DRD"
__maintainer__ = __author__
__credits__ = __author__

__url__ = "https://github.com/RuanMiguel-DRD/You-MP3"
__email__ = "ruanmigueldrd@outlook.com"

__keywords__ = [
    # Categories
    "audio", "conversion", "downloader", "music",

    # Dependencies
    "ffmpeg", "mutagen", "pillow", "yt-dlp",

    # Others 
    "metadata", "youtube", "mp3"
]

# Imports

from .downloader import Setting, download_music, extract_playlist
from .metadata import add_metadata, create_cover

__all__ = [
    "Setting", "download_music", "extract_playlist",
    "add_metadata", "create_cover"
]
