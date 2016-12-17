#!/bin/bash

flacdir="$1"
echo "$flacdir"

remove_flac=`echo $flacdir | sed -e "s/[[(]*\<FLAC\>[])]*//" -e "s/[[(]*\<flac\>[])]*//"`

v0dir=""${remove_flac/\//}" [V0]" 
v2dir=""${remove_flac/\//}" [V2]" 
maxdir=""${remove_flac/\//}" [320]"

cp_non_flac()
{

    # Copy all of the remaining files into each subdirectory
    #for x in `find "$flacdir" -maxdepth 1 ! -iname "*.flac"`; do
    for x in `ls "$flacdir" | grep -v "flac$"`; do
        cp -r "$flacdir"/"$x" "$v0dir"
        cp -r "$flacdir"/"$x" "$v2dir"
        cp -r "$flacdir"/"$x" "$maxdir"
    done
}

mkdir -p "${v0dir}"
mkdir -p "${v2dir}"
mkdir -p "${maxdir}"

for f in "$flacdir"*.flac; do
    outmp3=`echo "${f%.*}.mp3" | cut -d/ -f2`
    ffmpeg -i "$f" -codec:a libmp3lame -q:a 0 "$v0dir"/"$outmp3"
    ffmpeg -i "$f" -codec:a libmp3lame -q:a 2 "$v2dir"/"$outmp3"
    ffmpeg -i "$f" -codec:a libmp3lame -b:a 320k "$maxdir"/"$outmp3"
done

cp_non_flac
