# 結晶領域、線分検出プログラム

## 使用言語
python 3.10.13
## 使用ライブラリ
opencv 4.6.0  
matplotlib 3.8.3  
ocrd-fork-pylsd 0.0.8
numpy 1.24.3  

## 各ディレクトリ、プログラムファイルの説明
### libディレクトリ
メインプログラムで利用する関数群が入ったディレクトリ
### modelディレクトリ
学習させたモデルを利用するためのクラスファイルを格納しているディレクトリ
### parameterディレクトリ
学習させたモデルのパラメータファイルを保持するためのディレクトリ
### imgディレクトリ
プログラムで利用する画像、および出力される画像を保存するためのディレクトリ
### メインプログラム
region_detector.py:領域検出プログラム。  
calc_acc.py:検出した領域の精度を求めるためのプログラム。  
one_dot_region_fillter.py:検出した領域について、飛び飛びになっている領域を塗りつぶすプログラム。  
line_distribution_detector.py:結晶領域に含まれる線分の分布を求めるプログラム。分布はグラフ画像として出力される。
