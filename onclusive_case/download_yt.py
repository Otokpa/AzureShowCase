import sys
import os
from pytube import YouTube
from pytube.exceptions import VideoUnavailable


def get_video(url, audio_only=False):

    try:
        yt = YouTube(url)

    except VideoUnavailable:
        print(f'Video {url} is unavailable.')
        sys.exit()
    else:

        if audio_only:
            print(f'Downloading audio of video: {url}')
            tag = yt.streams.filter(file_extension='mp4', mime_type='audio/mp4').first().itag
            stream = yt.streams.get_by_itag(tag)
        else:
            print(f'Downloading video: {url}')
            stream = yt.streams.get_highest_resolution()

        video_name = stream.title.replace(' ', '_') + '.mp4'
        text_name = stream.title.replace(' ', '_') + '.txt'

        directory = 'media/' + stream.title.replace(' ', '_')

        if not os.path.exists(directory):
            os.makedirs(directory)
            print("Directory created: ", directory)
            stream.download(directory, video_name)
        else:
            print("Directory already exists: ", directory)
            if os.path.exists(directory + '/' + video_name) and os.path.getsize(directory + '/' + video_name) > 0:
                pass
            else:
                stream.download(directory, video_name)

    video_path = directory + '/' + video_name
    text_path = directory + '/' + text_name

    return video_path, text_path

# url = 'https://www.youtube.com/watch?v=DVpTpx9Avf0'
#
# video_path, text_path = get_video(url)
