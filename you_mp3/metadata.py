"Module for handling metadata and creating covers"

from mutagen.mp3 import MP3
from mutagen.id3 import ID3
from mutagen.id3._frames import APIC, TALB, TCON, TDRC, TIT2, TPE1, TPE2, TRCK

from PIL import Image
from PIL.Image import Image as image

from os import system
from os.path import splitext

from .__utils import ffmpeg_check


def add_metadata(mp3_path: str, metadata: dict[str, str | bytes]) -> None:
    """Add metadata to an mp3 file

    Args:
        mp3_path: string containing the path to the mp3 file
        If you do not specify a valid path, an empty file containing the metadata will be generated instead
        metadata: structured dictionary containing the metadata

    Metadata:
        Mandatory metadata are:
            - artist: string containing artist or band name
            - title: string containing song name
            - date: string containing song release date in (year-month-day) format

        For gender:
            - genre: string containing the musical genres of the song

        For album metadata:
            - album: string containing album name
            - artist-album: string containing the name of the album's artist
            - track-number: string containing track number
            - track-total: string containing total number of tracks

        For cover:
            - cover: binary data containing the cover image
    """

    # Although EasyID3 exists, which is a simpler interface, we use traditional ID3 for compatibility and flexibility reasons
    metadata_handler = ID3()

    metadata_handler["TPE1"] = TPE1(text=metadata["artist"])
    metadata_handler["TIT2"] = TIT2(text=metadata["title"])
    metadata_handler["TDRC"] = TDRC(text=metadata["date"])

    if "genre" in metadata:
        metadata_handler["TCON"] = TCON(text=metadata["genre"])

    if "album" in metadata:
        metadata_handler["TALB"] = TALB(text=metadata["album"])
        metadata_handler["TPE2"] = TPE2(text=metadata["artist-album"])
        metadata_handler["TRCK"] = TRCK(text=f'{metadata["track-number"]}/{metadata["track-total"]}')

    if "cover" in metadata:
        metadata_handler["APIC"] = APIC(
                desc="Image cover of music",
                data=metadata["cover"],
                mime="image/jpeg",
                type=0
            )

    metadata_handler.save(mp3_path)


def create_cover(image_path: str, image_size: tuple[int, int] = (600, 600)) -> str:
    """Creates a jpeg cover to be implemented in mp3 files

    Args:
        image_path: string containing path to the image that will generate a cover
        image_size (optional): tuple containing the height and width of the image in integers

    Returns:
        str: path of the created cover image file
    """

    image_data: image = Image.open(image_path)

    if image_data.mode == "RGBA":
        background: image = Image.new("RGB", image_data.size, (255, 255, 255))
        background.paste(image_data, mask=image_data.split()[3])
        image_data = background

    image_data = image_data.resize(image_size)

    file_name: str
    file_name, _ = splitext(image_path)
    file_name += ".cover.jpeg"

    image_data.save(file_name, "JPEG")

    return file_name


def trim_music(mp3_path: str, start: int = 0, end: int = 0, debug: bool = False) -> str:
    """Cut out a section of the music

    Args:
        mp3_path: string containing the path to the mp3 file
        start: time in seconds from where the music should start
        end: time in seconds from where the music should end
        debug (optional): boolean to define whether or not to enable debugging

    Returns:
        str: string with the music path after the cuts

    Raises:
        ValueError: when providing invalid values, such as start and end with 0, a start value greater than the end value, or an end greater than the duration of the music
    """

    if start == 0 and end == 0:
        raise ValueError("You need to pass a value to start or end")

    new_path: str
    new_path, _ = splitext(mp3_path)
    new_path += ".trim.mp3"

    mp3_file: MP3 = MP3(mp3_path)

    if end == 0:
        end = mp3_file.info.length

    if start < end:

        if mp3_file.info.length >= end:

            command: str = f"ffmpeg -i \"{mp3_path}\""

            if start != 0:
                command += f" -ss {start}"

            if end != mp3_file.info.length:
                command += f" -to {end}"

            command += f" -c copy \"{new_path}\" -loglevel "

            if debug == True:
                command += "info"

            else:
                command += "quiet"

            ffmpeg_check(None)

            system(command)

            return new_path

        else:
            raise ValueError("Ending time greater than the total time of the music")

    else:
        raise ValueError("The start time is after the end time")
