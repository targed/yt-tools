import click
from credentials import *
from addVideoToPlaylist import *
from addCSVToPlaylist import *
from exportPlaylist import *
from exportVideo import *


@click.group()
def cli():
    pass


@cli.command("playlist", help="Export a playlist as a CSV")
@click.option(
    "--playlistid",
    type=str,
    default="PLFfbfebe4m0iSzzCXos7jZRPcOSfvYX65",
    help="Input the unique playlist id. This can be found in the address bar (Example: https://www.youtube.com/playlist?list=YOURPLAYLISTID) This does not work with watch later",
)
def exepid(playlistid):
    playlistid = str(playlistid)
    process_playlist(playlistid)


@cli.command("video", help="Retrieve information about a specific YouTube video")
@click.option(
    "--videoid",
    type=str,
    default="dQw4w9WgXcQ",
    help="Input the unique video id. This can be found in the address bar (Example: https://www.youtube.com/watch?v=YOURVIDEOID)",
)
def exevid(videoid):
    videoid = str(videoid)
    process_video(videoid)


@cli.command("addvideo", help="Add a video to an already existing playlist")
@click.option(
    "--videoid",
    type=str,
    default="dQw4w9WgXcQ",
    help="Input the unique video id. This can be found in the address bar (Example: https://www.youtube.com/watch?v=YOURVIDEOID)",
)
@click.option(
    "--playlistid",
    type=str,
    default="PLFfbfebe4m0iSzzCXos7jZRPcOSfvYX65",
    help="Input the unique playlist id. This can be found in the address bar (Example: https://www.youtube.com/playlist?list=YOURPLAYLISTID) This does not work with watch later",
)
def exevpid(videoid, playlistid):
    videoid = str(videoid)
    playlistid = str(playlistid)
    add_video_to_playlist(youtube, videoid, playlistid)


@cli.command(
    "addcsv", help="Add a list of YouTube videos to an already existing playlist"
)
@click.option(
    "--playlistid",
    type=str,
    default="PLFfbfebe4m0iSzzCXos7jZRPcOSfvYX65",
    help="Input the unique playlist id. This can be found in the address bar (Example: https://www.youtube.com/playlist?list=YOURPLAYLISTID) This does not work with watch later",
)
def exevpid(playlistid):
    playlistid = str(playlistid)
    addCSV(playlistid)


if __name__ == "__main__":
    cli()
