# ダイビングの動画から魚が写っている部分を切り取る

## 概要

ダイビング中に動画を撮影する場合、カメラを回しっぱなしにしておくことも多く、写真用に動画から画像を切り抜くときに魚が写っている部分を切り抜く作業を自動化できないかと思ったのでPythonを使って作成してみました。

OpenCVによる動体検知とCNNを使った画像分類を用いてダイビングの動画から魚が写っているフレームを切り取って保存するコードを作成し、Flaskでweb上でも使えるようにしました。

処理されている様子がわかるように動体検知している様子(動きのある部分を緑の枠で囲む)をwebページ上に表示しています。

**処理の流れ**

ファイルをアップロード

↓

OpenCVで前後のフレームの差分を見て、ある程度の大きさで動きがある部分を検知

↓

動きがあった部分に魚が写っているかどうかをCNNで判断

↓

魚が写っている部分が一定数あればそのフレームをフォルダに保存


## DEMO

動きのある部分が緑の枠で囲まれる

![ezgif com-gif-maker (3)](https://user-images.githubusercontent.com/73343411/126371492-6182084b-07ff-4476-abfb-b090c241be20.gif)

30秒ほどの動画から40枚程度の画像が保存された

<img width="400" alt="スクリーンショット 2021-07-21 2 53 57" src="https://user-images.githubusercontent.com/73343411/126372288-c0b7d3a3-ec17-45b9-aba8-94d72ac99126.png">

<img width="300" src="https://user-images.githubusercontent.com/73343411/126372354-d061b400-1917-4e46-ba10-f4ffd0c2e32c.jpg"><img width="300" src="https://user-images.githubusercontent.com/73343411/126372425-73d77a6d-8e7b-4c5f-aab6-3997e11cc28c.jpg">

## 各ファイルの説明

**main.py**

>Flaskでルーティングを設定
>
> "/upload"でアップロードされたファイルを保存してそのパスをget_movie.pyに渡す
> 
> "/video_feed"で処理された画像をweb上に表示
>
> templatesフォルダにはブラウザで表示するhtmlファイル、staticフォルダにはcssのファイルがある
> 
> コマンドラインで`python main.py`から実行し、http://localhost:5000
> で表示

**get_movie.py**

>アップロードされた画像を処理&yieldを使ってフレームごとの画像を返す

**cvt_npz.py**
>CNNモデルが画像を学習できるように画像情報を配列に変換しバイナリファイルとして保存する
>
>魚が写っていない画像をimage/nofish、写っている画像をimage/fishフォルダに保存してnofishに0、fishに１のラベルを付けてそれらをまとめてimage/photos.npzに出力

**nn_model.py**

>画像の学習に使ったCNNのモデル
>
>cvt_npz.pyで作成したphotos.npzを元に学習を行う
>
>モデルの階層情報はfind_fish_model.jsonに、モデルの各層の重みはfind_fish_weight.hdf5に出力

**image_download.py**
>flickr APIを使ってモデルの学習に必要な画像を集める事ことができる
>
>"検索ワード"に集めたい画像の種類、"ディレクトリ名"に画像を保存するパスをいれてコマンドラインから実行
>
>今回は自分で撮影した動画やフリーのダイビング動画をダウンロードしたものを中心にモデルの学習をおこなった

[Flickr](https://www.flickr.com/)

## 環境

anaconda環境を使用

conda : 4.10.1

python 3.8

opencv-python : 4.5.3.56

tensolflow : 2.5.0

keras : 2.4.3
