# importing packages
import os, csv, time, sys
from pytube import YouTube 
from moviepy.editor import AudioFileClip
import mutagen
from mutagen.easyid3 import EasyID3


def download_youtube_audio(destination, csv_file):
    # CSVファイルを開く
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file, delimiter='\t')

        # 各行を処理する
        for row in reader:
            # print(row)
            print(row['yt_url'])
            print(row['no'])
            print(row['artist'])
            print(row['title'])
            print(row['album'])

            # delete old file if exists
            if os.path.exists(destination + "/" + row['title'] + ".mp3"):
                os.remove(destination + "/" + row['title'] + ".mp3")
                print("Deleted old file")

            yt = YouTube(row['yt_url'])

            # extract only audio
            video = yt.streams.filter(only_audio=True).first()

            temp_file = video.download()
            audio_clip = AudioFileClip(temp_file)
            audio_clip.write_audiofile(destination + "/" + row['title'] + ".mp3", codec="libmp3lame")

            while os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                except PermissionError:
                    time.sleep(1)  # 他のプロセスが解放するまで待つ
                    print("sleeping...")

            # result of success
            print(yt.title + " has been successfully downloaded.")

            # Update mp3 Metadata
            tags = mutagen.File(destination + "/" + row['title'] + ".mp3", easy=True)
            tags['tracknumber'] = str(row['no'])
            tags['artist'] = row['artist']
            tags['title'] = row['title']
            tags['album'] = row['album']
            tags.save(destination + "/" + row['title'] + ".mp3")
            changed = EasyID3(destination + "/" + row['title'] + ".mp3")
            print(changed)


if __name__ == "__main__":
    # コマンドライン引数から出力先とCSVファイルを取得
    if len(sys.argv) < 3:
        print("Usage: python main.py <destination_directory> <csv_file>")
        print("Example: python main.py ./output kumon_1.csv")
        sys.exit(1)
    
    destination = sys.argv[1]
    csv_file = sys.argv[2]
    
    # 出力ディレクトリが存在しない場合は作成
    if not os.path.exists(destination):
        os.makedirs(destination)
    
    download_youtube_audio(destination, csv_file)
