from edit import recognition, make_movie
path = "Jim Carrey Speech At The Golden Globe Awards 2016  HDTV.mp4"
all_word = recognition(path)
print(all_word)
#入れ子になってる配列をならすとき、後ろに連ねてく
texts = [word for words in all_word['segments'] for word in words['words']]
movie = make_movie(path,texts)
# [text['word'],text['start'],text['end'] for text in texts]


######

#使っているライブラリを正しく動かすためにやったこと

######
#whisperをインストールするためにgitから直接入れるコマンドを打ち
#pip install git+https://github.com/openai/whisper.git

# バージョンの互換性から古いバージョンのtorch(コンパイラー？)を入れて動作させた
# pip install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cpu

#動画を読み込むためにFFMpegが必要なので
#ffmpeg-master-latest-win64-gplのFFMpegをダウンロード

#その後moviepyを動作するため動画ファイルの読み込みのためのImageMageckをダウンロード
#ImageMagick-7.1.1-Q16
