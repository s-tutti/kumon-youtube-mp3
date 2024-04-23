# importing packages
import os, csv, time
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
    destination = "C:/tmp/tmp_20240420_205830/mp3"
    csv_file = "kumon_1.csv"
    # csv_file = "kumon_2-5.csv"
    download_youtube_audio(destination, csv_file)
