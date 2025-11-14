import sys
from pytube import Playlist, YouTube

def get_video_info(playlist_url):
    playlist = Playlist(playlist_url)
    video_info = []
    for i, url in enumerate(playlist.video_urls, start=1):
        video = YouTube(url)
        video_info.append((i, video.title, url))
    return video_info

if __name__ == "__main__":
    # コマンドライン引数からプレイリストURLを取得
    if len(sys.argv) < 2:
        print("Usage: python getUrlFromPlayList.py <playlist_url>")
        print("Example: python getUrlFromPlayList.py 'https://www.youtube.com/playlist?list=YOUR_PLAYLIST_ID'")
        sys.exit(1)
    
    playlist_url = sys.argv[1]
    video_info = get_video_info(playlist_url)

    for track_number, title, url in video_info:
        print(f"{track_number},{title},{url}")
