"Internal module and library utilities"

from re import match as pattern # Match function alias for pattern to avoid conflicts with match/case structure

from shutil import which

from typing import Any


ERROR_TYPE: str = "Unexpected primitive type"
"Error message if the data variable has a value with an incorrect primitive type"


def ffmpeg_check(config: dict[str, Any] | None = None) -> None:
    """Function to check if ffmpe_location is set correctly

    Args:
        config: YoutubeDL configuration dictionary
        If you pass None to the config variable, the function will search for ffmpeg in the system

    Raises:
        OSError: the binary \"ffmpeg\" was not found on the system
        KeyError: key \"ffmpeg_location\" is not defined in the dictionary
        TypeError: key \"ffmpeg_location\" is defined without a value
    """

    if type(config) == None:
        if not which("ffmpeg"):
            raise OSError("\"ffmpeg\" binary not found on your system")

    elif type(config) == dict:

        try:
            if type(config["ffmpeg_location"]) != str:
                raise TypeError

        except (KeyError):
            raise KeyError("\"ffmpeg_location\" key not set")

        except (TypeError):
            raise TypeError("\"ffmpeg_location\" key set with invalid value")


def format_time(time: str) -> int:
    """Function to format time in whole seconds

    Args:
        time: string with a time in the format HH:MM:SS

    Raises:
        TypeError: if the time string is not in any compatible format

    Returns:
        int: time converted to total seconds
    """

    hours: int
    minutes: int
    seconds: int

    if pattern(r"^\d{1,2}:\d{2}:\d{2}$", time):
        hours, minutes, seconds = map(int, time.split(':'))
        return hours * 3600 + minutes * 60 + seconds

    elif pattern(r"^\d{1,2}:\d{2}$", time):
        minutes, seconds = map(int, time.split(':'))
        return minutes * 60 + seconds

    elif pattern(r"^\d+$", time):
        seconds = int(time)
        return seconds

    else:
        raise TypeError("The string does not contain a valid time format")
