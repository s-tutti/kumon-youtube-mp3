from pytube import Playlist, YouTube

def get_video_info(playlist_url):
    playlist = Playlist(playlist_url)
    video_info = []
    for i, url in enumerate(playlist.video_urls, start=1):
        video = YouTube(url)
        video_info.append((i, video.title, url))
    return video_info

# プレイリストのURLを指定します。
playlist_url = 'https://www.youtube.com/playlist?list=PLuQoiXkVnkQPuiGtEjduxcrZUK5mqjG5j'
video_info = get_video_info(playlist_url)

for track_number, title, url in video_info:
    print(f"{track_number},{title},{url}")

