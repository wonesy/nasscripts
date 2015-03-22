#!/usr/bin/python

import os
import re
import sys
import eyed3
import shutil
import time

g_dl_dir = "/media/apricot/torrents/download/"
#g_dl_dir = "/home/camomile/"

g_tv_dir = "/media/blackberry/TV Shows/"
#g_tv_dir = "/home/camomile/tv/"

g_music_dir = "/media/blackberry/music/"
#g_music_dir = "/home/camomile/music/"

g_movie_dir = "/media/blackberry/Movies/"
#g_movie_dir = "/home/camomile/movies/"

g_norg_log = "/home/camomile/.log/norganize.log"

g_music_mimes = [
    ".mp3",
    ".flac",
]

g_video_mimes = [
    ".avi",
    ".mp4",
    ".mkv",
]

g_target = sys.argv[1]
now = time.strftime("%m-%d-%Y @ %H:%M:%S ")

log = open(g_norg_log, "a")

# Init
mimes_present = {}

def play_that_funky_music():
    artists = {}

    # Get artists name
    for fn in os.listdir('.'):
        name, ext = os.path.splitext(fn)

        # Save each artist found
        if ext in g_music_mimes:
            audio = eyed3.load(fn)
            val = artists.setdefault(audio.tag.artist, 0)
            artists[audio.tag.artist] = val + 1
            album_name = audio.tag.album
            album_date = audio.tag.getBestDate()

    # Single artist?
    if len(artists) == 1:
        album_artist = artists.keys()[0]
    else:
        album_artist = 'Various Artists'

    # Check if artist dir already exists
    if not os.path.isdir(g_music_dir + album_artist):
        os.mkdir(g_music_dir + album_artist, 0777)
        log.write(now + "Making Album Path " \
            + g_music_dir + album_artist + "\n")

    if album_date:
        album_dir_name = "%s (%d)" % (album_name, album_date.year)
    else:
        album_dir_name = album_name

    # Check if album dir already exists
    full_album_path = g_music_dir + album_artist + "/" + album_dir_name
    if not os.path.isdir(full_album_path):
        os.mkdir(full_album_path, 0777)

    # Now we have the proper directory!
    for fn in os.listdir('.'):
        shutil.copy(fn, full_album_path)

    log.write(now + "[MUSIC] Created directory " + full_album_path + "\n")

def lights_camera_action():
    pass

def netflix_couch_potato():
    pass

# Move to completed target dir
os.chdir(g_dl_dir + g_target)


# Gather all mime types
nummusic = 0
numvideo = 0

for fn in os.listdir('.'):
    name, ext = os.path.splitext(fn)

    if ext in g_music_mimes:
        nummusic += 1
    elif ext in g_video_mimes:
        numvideo += 1
    else:
        # chances are it's a missing video type :(
        numvideo +=1

# Make an educated guess if music/movie/tv
# Assumptions:
#       - anything with mp3, flac = music
#       - anything with <= 2 video files is (probably) a movie
#       - all else with video > 2 is TV
if nummusic > numvideo:
    play_that_funky_music()
elif numvideo > 0 and numvideo <= 2:
    lights_camera_action()
elif numvideo > 2:
    netflix_couch_potato()
else:
    log.write(now + "Error: Could not determine the type of torrent!\n")

