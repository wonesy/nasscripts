#!/usr/bin/python

import os
import re
import sys
import eyed3
import shutil
import time
import guessit

# Something weird about encoding
reload(sys)
sys.setdefaultencoding('utf-8')

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
        log.write(now + "Making Artist Path " + g_music_dir + album_artist + "\n")

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

def netflix_couch_potato():
    for root, dirs, files in os.walk(os.getcwd()):
        guess = []
        home_found = False
        homeless_files = []
        dest_fullpath = ""

        for fn in files:
            fullpath = os.path.join(root, fn)
            name, ext = os.path.splitext(fn)
            
            if not home_found:
                if ext == ".nfo":
                    continue
                homeless_files.append(os.path.join(root, fn))

            if home_found:
                shutil.copy(os.path.join(root, fn), dest_fullpath)
                continue

            if ext in g_video_mimes:
                home_found = True
                guess = guessit.guess_file_info(fullpath)
                series = guess['series']
                season = guess['season']

                if not os.path.isdir(g_tv_dir + series):
                    log.write(now + "[TV] Created directory " + series)
                    os.mkdir(g_tv_dir + series)

                if not os.path.isdir(g_tv_dir + series + "/Season " + str(season)):
                    log.write(now + "[TV] Created directory " + series + " " + str(season))
                    os.mkdir(g_tv_dir + series + "/Season " + str(season))

                dest_fullpath = g_tv_dir + series + "/Season " + str(season)

        for hobos in homeless_files:
            print hobos
            print dest_fullpath
            shutil.copy(hobos, dest_fullpath)

    pass

def lights_camera_action():
    # assumes there is at most one directory

    target_full_path = g_dl_dir + "/" + g_target
    guess = []

    # is a directory
    if os.path.isdir(target_full_path):
        for fn in os.listdir('.'):
            name, ext = os.path.splitext(fn)

            if ext in g_video_mimes:
                guess = guessit.guess_file_info(g_dl_dir + "/" + fn)
                break

        mv_title = guess['title']
        mv_year = guess['year']

        if mv_year:
            mv_link_name = g_movie_dir + mv_title + " (" + mv_year + ")"
        else:
            mv_link_name = g_movie_dir + mv_title

        os.symlink(target_full_path, mv_link_name)

    # was originally just a single video file
    else:
        guess = guessit.guess_file_info(target_full_path)

        mv_title = guess['title']
        mv_year = guess['year']

        if mv_year:
            mv_link_name = g_movie_dir + mv_title + " (" + mv_year + ")"
        else:
            mv_link_name = g_movie_dir + mv_title

        os.mkdir(mv_link_name)
        shutil.copy(target_full_path, mv_link_name)

# Gather all mime types
def get_torrent_type():

    # Move to completed target dir
    if os.path.isdir(g_dl_dir + g_target)
        os.chdir(g_dl_dir + g_target)
        for root, dirs, files in os.walk(os.getcwd()):
            for fn in files:
                name, ext = os.path.splitext(fn)
                fullpath = os.path.join(root, fn)

                if ext in g_video_mimes:
                    guess = guessit.guess_file_info(fullpath)
                    vid_type = guess['type']
                    return vid_type
                elif ext in g_music_mimes:
                    return 'music'
    else:
        name, ext = os.path.splitext(g_target)
        if ext in g_video_mimes:
            guess = guessit.guess_file_info(g_dl_dir + g_target)
            vid_type = guess['type']
            return vid_type
        elif ext in g_music_mimes:
            return 'music'

    return 'unknown'



torrent_type = get_torrent_type()

if torrent_type == "music":
    play_that_funky_music()
elif torrent_type == "episode":
    netflix_couch_potato()
elif torrent_type == "movie":
    lights_camera_action()
else:
    msg = "Unknown torrent type: " + torrent_type + " (" + g_target + ")"
    print msg
    log.write(now + msg)
