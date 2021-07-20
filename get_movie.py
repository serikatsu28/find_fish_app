import cv2, os, copy
from keras.models import model_from_json

class GetMovie():
    # 保存したモデルの読み込み
    nn_model = model_from_json(open('find_fish_model.json', 'r').read())
    # 保存した学習済みの重みを読み込み
    nn_model.load_weights('find_fish_weight.hdf5')

    movie_path = ''
    cap = cv2.VideoCapture(movie_path)

    @staticmethod
    def capture_bestshot():

        img_row = 64
        img_col = 32
        color = 3
        count = 0
        frame_count = 0
        img_last = None # 前回の画像
        border = 5 # 画像を出力するかどうかのしきい値
        output_dir = './bestshot'

        if not os.path.isdir(output_dir):
            os.mkdir(output_dir)

        while True:
            # 画像を取得
            ret, frame = GetMovie.cap.read()
            if not ret:
                break
            frame = cv2.resize(frame, (640, 360))
            frame2 = copy.copy(frame)
            frame_count += 1
            # 前フレームと比較するために白黒に変換
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (15, 15), 0)
            img_b = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)[1]
            if not img_last is None:
                # 差分を得る
                frame_diff = cv2.absdiff(img_last, img_b)
                diff_area = cv2.findContours(frame_diff,
                    cv2.RETR_EXTERNAL,
                    cv2.CHAIN_APPROX_SIMPLE)[0]
                # 差分領域に魚が映っているか調べる
                fish_count = 0
                for area in diff_area:
                    x, y, w, h = cv2.boundingRect(area)
                    if w < 100 or w > 500: # ノイズを除去
                        continue
                    # 抽出した領域に魚が映っているか確認
                    image = frame[y:y+h,x:x+w]
                    image = cv2.resize(image, (img_row,img_col))
                    image_data = image.reshape(-1, img_row, img_col, color) / 255
                    y_pred = GetMovie.nn_model.predict_classes([image_data])
                    if y_pred[0] == 1:
                        fish_count += 1
                        cv2.rectangle(frame2, (x, y), (x+w, y+h), (0,255,0), 2)
                # 魚が映っているかどうか
                if fish_count > border:
                    fname = output_dir + '/fish' + str(count) + '.jpg'
                    cv2.imwrite(fname, frame)
                    count += 1

            img_last = img_b

            ret, frame2_jpeg = cv2.imencode('.jpg', frame2)
            frame2_jpeg = frame2_jpeg.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame2_jpeg + b'\r\n\r\n')

        print('ベストショット数', count, '/', frame_count)
