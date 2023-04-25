from pathlib import Path
from time import time, sleep
import os

from threading import Thread
import ffmpeg
from yt_dlp import YoutubeDL
import cv2

from scheme import time_scheme

threads = []
video_ext = ['.mp4', '.mkv', '.webm']

def video_splitter(video_path : Path = Path('video.mp4'), output_path : Path = None, start_time : time_scheme = time_scheme(hh=00,mm=00,ss=00), end_time : time_scheme = time_scheme(hh=00,mm=00,ss=00), output_dir : Path = Path('split_output')):
    if not output_dir.exists():
        output_dir.mkdir()
    if not video_path.exists():
        raise FileNotFoundError(f'File {video_path} not found')
    if output_path is None:
        output_path = Path(f'{video_path.stem}_{start_time.__to_str_seconds__()}_{end_time.__to_str_seconds__()}.mp4')
    if (output_dir / output_path).exists():
        return ValueError(f'File {(output_dir/output_path).name} already exists')
    if start_time.__to_seconds__() > end_time.__to_seconds__():
        raise ValueError('Start time is bigger than end time')
    if start_time.__to_seconds__() < 0 or end_time.__to_seconds__() < 0:
        raise ValueError('Start time or end time is less than 0')
    if start_time.__to_seconds__() == end_time.__to_seconds__():
            raise ValueError('Start time is equal to end time')
    ffmpeg.output(ffmpeg.input(filename=video_path), filename=f'{output_dir.name}\\{output_path.name}', ss=start_time.__to_seconds__(), t=round(end_time.__to_seconds__() - start_time.__to_seconds__())).run()

def cleanUp(dir : Path = Path('split_output')):
    for file in dir.iterdir():
        file.unlink()

def youtube_url_validator(youtube_url : str) -> YoutubeDL.extract_info:
    info = YoutubeDL().extract_info(youtube_url, download=False)
    if info is None:
        return False
    return info

def youtube_video_downloader(video_url : str, output_dir : Path = Path('download_output')):
    info = youtube_url_validator(youtube_url=video_url)
    if not info:
        raise ValueError('Video url is not valid')
    if not output_dir.exists():
        output_dir.mkdir()
    if not output_dir.is_dir():
        raise ValueError('Output dir is not a directory')
    
    uuid = info.get('id', None)
    if uuid is None:
        raise ValueError('UUID is None')
    
    with YoutubeDL({'outtmpl': f'{output_dir.name}\\{uuid}.%(ext)s'}) as ydl:
        ydl.download([video_url])
    
    return uuid

def youtube_video_generator(youtube_url : str = None, output_dir : Path = Path('download_output'), step : int = 10):
    cleanUp()
    if youtube_url is None:
        pass
    uuid = youtube_video_downloader(video_url=youtube_url, output_dir=output_dir)
    video = None
    for file in output_dir.iterdir():
        if file.stem == uuid and file.suffix in video_ext:
            video = file
            break
    if video is None:
        raise FileNotFoundError('Video not found')
    
    vid = cv2.VideoCapture(f'{output_dir.name}\\{video.name}')

    fps = vid.get(cv2.CAP_PROP_FPS)
    length = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = round(length/fps)
    for i in range(0, duration, step):
        start_time = time_scheme(hh=0,mm=0,ss=i)
        end_time = time_scheme(hh=0,mm=0,ss=i+step)
        t = Thread(target=video_splitter, args=(video, None, start_time, end_time, Path('split_output')))
        t.start()
        threads.append(t)

if __name__ == '__main__':
    youtube_url = 'https://www.youtube.com/watch?v=QH2-TGUlwu4&ab_channel=NyanCat'
    youtube_video_generator(youtube_url=youtube_url)