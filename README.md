# You-MP3

The tool for downloading music from YouTube

The program is an abstraction and simplification layer of yt-dlp, along with some uses of ffmpeg

I initially created this project because I was dissatisfied with traditional music downloaders that did not add metadata to the songs, did not have a clipping function, or were too complex instead of having a simple command line interface

## Metadata

The tool automatically adds metadata to downloaded songs using information provided by the platform from which the songs are being downloaded

| Metadata     | Origin of metadata                                                 |
|--------------|--------------------------------------------------------------------|
| Artist       | Channel name                                                       |
| Title        | Video name                                                         |
| Date         | Publication date                                                   |
| Cover        | Video thumbnail                                                    |
| Album        | Playlist name                                                      |
| Artist Album | Playlist creator name                                              |
| Track Number | total number of videos in the playlist and the index of each video |
| Genre        | Provided by the user on the command line                           |

Some metadata is not added for a number of reasons, such as lack of relevance, platform incompatibility, among other reasons

Among the metadata not added, we have the lyric metadata, which could be added using the video subtitles as the source, but it was not because YouTube provides several different subtitle formats for each video, and each format would require different data processing, which would make the program much more complex than planned

## Limitations

Not all mp3 players are fully compatible with ID3 model metadata, which may result in some metadata not being read or the cover image not being displayed

The program was designed to be used on YouTube, it can be used on other platforms, but with the risk of malfunction or partial functioning
