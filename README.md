# 結晶領域、線分検出プログラム

## 使用言語
python 3.10.13
## 使用ライブラリ
opencv 4.6.0  
matplotlib 3.8.3  
ocrd-fork-pylsd 0.0.8
numpy 1.24.3  

※なお、筆者は仮想環境構築のために標準ライブラリであるvenvを用いています。

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
<table>
    <thead>
        <tr>
            <th>プログラム名</th>
            <th>説明</th>
        </tr>
    </thead>
    <tr>
        <th>region_detector.py</th>
        <th>領域検出プログラム。</th>
    </tr>
    <tr>
        <th>calc_acc.py</th>
        <th>検出した領域の精度を求めるためのプログラム。 </th>
    </tr>
    <tr>
        <th>one_dot_region_fillter.py</th>
        <th>検出した領域について、飛び飛びになっている領域を塗りつぶすプログラム。</th>
    </tr>
    <tr>
        <th>line_distribution_detector.py</th>
        <th>結晶領域に含まれる線分の分布を求めるプログラム。分布はグラフ画像として出力される。</th>
    </tr>
    <tr>
        <th>annotation_search.py</th>
        <th>アノテーション用の画像を作成するためのプログラム（未完成）。</th>
    </tr>
</table>
