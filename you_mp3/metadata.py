"Module for handling metadata and creating covers"

from mutagen.id3 import ID3
from mutagen.id3._frames import APIC, TALB, TCON, TDRC, TIT2, TPE1, TPE2, TRCK

from PIL import Image

from os import remove
from os.path import splitext


def add_metadata(mp3_path: str, metadata: dict[str, str | bytes]) -> None:
    """Add metadata to an mp3 file

    Args:
        mp3_path: string containing the path to the mp3 file
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
                data=metadata["cover"],
                mime="image/jpeg",
                type=0
            )

    metadata_handler.save(mp3_path)


def create_cover(image_path: str, image_size: tuple[int, int] = (600, 600), delete_original: bool = True) -> str:
    """Creates a jpeg cover to be implemented in mp3 files

    Args:
        image_path: string containing path to the image that will generate a cover
        image_size (optional): tuple containing the height and width of the image in integers
        delete_original (optional): boolean to define whether or not the original file should be deleted during conversion

    Returns:
        file_name: string containing the path of the created cover file

    If you do not specify a valid path, an empty file containing the metadata will be generated instead.
    """

    image_data = Image.open(image_path)
    image_data = image_data.resize(image_size)

    file_name: str
    file_name, _ = splitext(image_path)

    if delete_original:
        file_name = f"{file_name}.jpeg"
        remove(image_path)

    else:
        file_name = f"{file_name}.cover.jpeg"

    image_data.save(file_name, "JPEG")

    return file_name
