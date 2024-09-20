import os
import glob
import json
import pdb
os.environ["IMAGEMAGICK_BINARY"] = "C:/Program Files/ImageMagick-7.1.1-Q16/magick.exe"
import moviepy.editor as mp
import moviepy.editor
import moviepy.video
import moviepy.video.VideoClip
import whisper
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

from moviepy.editor import *
from moviepy.video.VideoClip import VideoClip

from pathlib import Path
import numpy as np
MEDIA_ROOT = os.path.join(Path(__file__).resolve().parent.parent, 'media')
#ファイルから音声認識して単語ごと秒数を記録
def recognition(path):
    files:list[str] = [path]
    model = whisper.load_model('base.en')
    for i, file in enumerate(files):
        print("## {}".format(file))
        result = model.transcribe(file, language='en', verbose=True, word_timestamps=True)
        # pdb.set_trace()
        result['segments']
    return result

#もし処理元のファイルが動画なら
#動画を生成、編集して単語ごとにテキストを表示
def make_movie(path,texts):
    clip = VideoFileClip(path)
    final_clip = VideoFileClip(path).subclip(0,1)
    # before_last = texts[0]['start']
    array = [clip]
    #単語ごとのテキストデータを秒数事にclipに書き込みそれをつなげて１つの動画にする
    for text in texts:
        #その単語のテキストを生成
        start_second = float(text['start'])
        end_second = float(text['end'])
        txtclip = TextClip(text['word'],fontsize=120,color='white',stroke_width=5,stroke_color='black').subclip(start_second,end_second)
        txtclip = txtclip.set_start(start_second)
        #配列に順番に入れる
        array.append(txtclip)
    #元動画にテキストを挿入
    final_clip = CompositeVideoClip(array)
        
    #動画の書き出し
    media_path = MEDIA_ROOT + '\\media\\videos'
    # pdb.set_trace()
    file_name = os.path.basename(path)
    path_name = path.rsplit(file_name,1)[0]
    output_path = os.path.join(media_path, 'リオ式'+file_name)
    write = final_clip.write_videofile(output_path)
    return final_clip,output_path

# サムネイルを作るために動画の秒数で画像切り出し
def create_thumbnail(path):
    clip = VideoFileClip(path)
    root_path = os.path.splitext(path)[0].split('\\')
    file_name = root_path[-1] + "." + "jpeg"
    media_path = MEDIA_ROOT + '\\media\\images\\'
    output_path = os.path.join(media_path, 'リオ式'+file_name)
    clip.save_frame(output_path, t=1)
    return output_path