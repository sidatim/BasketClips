import ffmpeg
import random
import os
import streamlit as st
import pprint as pp
def check_for_audio(streams):
    for stream in streams:
        if not stream['streams']:
            return False
    return True
def export_video(videoEvents):
    videos = [video['videoUrl'] for video in videoEvents  if video['videoUrl']   ]
    if not videos:
        return "No videos to export."
    player = videoEvents[0]['player']
    gameid=videoEvents[0]['gameId']
    output_filename = f"{player}_{gameid}.mp4"
    try:
        proxy=random.choice(st.secrets["PROXY_LIST"]) if "PROXY_LIST" in st.secrets else None
        audioProbe=[ffmpeg.probe(video,
            headers="Accept: application/json, text/plain, */*\r\nAccept-Language: en-US,en;q=0.9\r\nReferer: https://www.nba.com/\r\n User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36\r\nx-nba-stats-origin: stats\r\nx-nba-stats-token: true\r\n",
        select_streams='a'
        )for video in videos]
        inputs = [
    ffmpeg.input(
        video,
        headers="Accept: application/json, text/plain, */*\r\nAccept-Language: en-US,en;q=0.9\r\nReferer: https://www.nba.com/\r\n User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36\r\nx-nba-stats-origin: stats\r\nx-nba-stats-token: true\r\n",
        #http_proxy=proxy
    
    ) for video in videos]
        video_streams = [inp.video for inp in inputs]
        audio_streams = [inp.audio for inp in inputs]
        valid_audio_streams=check_for_audio(audioProbe)
        if not valid_audio_streams:
            for i, audio in enumerate(audio_streams):
                audio_streams[i]=ffmpeg.input('anullsrc',)
        combined=[s for pair in zip(video_streams, audio_streams) for s in pair]
        if valid_audio_streams:
            (
            ffmpeg
            .concat(
                *combined,
                v=1,
                a=1,
            )
            .output(
               output_filename,
                vcodec='libx264',
                acodec='aac',
                video_bitrate='2000k',
                audio_bitrate='128k',
                r=30,    
            )
            .run(overwrite_output=True, capture_stdout=True, capture_stderr=True)
            )
        else:
            (
            ffmpeg
            .concat(
                *video_streams,
                v=1,
                a=0,
            )
            .output(
               output_filename,
                vcodec='libx264',
                r=30,    
            )
            .run(overwrite_output=True, capture_stdout=True, capture_stderr=True)
            )
        return output_filename
    except ffmpeg.Error as e:
        print("FFMPEG STDERR:")
        print(e.stderr.decode())
        if os.path.exists(output_filename):
            os.remove(output_filename)
        return -1