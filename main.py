import cv2, os
import datetime
import numpy as np
from flask import Flask, render_template, request, redirect, Response, make_response, jsonify, url_for
from werkzeug.utils import secure_filename
from get_movie import GetMovie

ALLOWED_EXTENSIONS = set(['mp4', 'wmv', 'avi', 'mov'])
UPLOAD_FOLDER = './uploads'
movie_path = ''

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allwed_file(filename):
    # .があるかどうかのチェックと、拡張子の確認
    # OKなら１、だめなら0
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#動画表示html
@app.route('/')
def index():
    return render_template('index.html')

#動画データ送信
@app.route('/video_feed')
def video_feed():
    get_movie = GetMovie()
    return Response(get_movie.capture_bestshot(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

#動画取得
@app.route('/upload', methods=["POST"])
def upload():
    if 'file' not in request.files: # ファイルがなかった場合
        print('ファイルがありません')
        redirect('/')
    file = request.files['file']    # データの取り出し
    if file.filename == '':         # ファイル名がなかった場合
        print('ファイルがありません')
        return redirect('/')
    if file and allwed_file(file.filename):
        filename = secure_filename(file.filename)   # 危険な文字を削除（サニタイズ処理）
        # ファイルを保存し、保存したファイルから動画読み出し
        if not os.path.isdir(UPLOAD_FOLDER):
            os.mkdir(UPLOAD_FOLDER)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        GetMovie.cap = cv2.VideoCapture(UPLOAD_FOLDER+"/"+filename)
        return redirect('/')
    else:
        print("not movie file")
        return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)  # http://localhost:5000で起動
