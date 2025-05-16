ペンタブレットの設定.
1. 常に値を取得し続ける
    ・ペンがタブレットに完全にくっついていなくてもマウスの位置を取得してしまうため, 接触ラベルがずれる可能性


<!-- 2. 接触した瞬間は取得しない
    ・カメラで取得したタイムスタンプと, ブラウザで取得した値を比べて, ブラウザで値が取得されていない間のものを接触ラベルにする -->

タブレット上でペンを動かすと, マウスの動きとして認識され, ブラウザ上でのマウスの座標が取得できるようになりました.
ペンがタブレットから離れているときは取得しないため, マウスの座標と一緒にタイムスタンプも取得し, それをカメラ画像から取得したペンの軌跡のタイムスタンプと比べることで, 接触か非接触かのラベルを自動で付けられるようになります.
 
来週は今週実装したものとカメラ画像からペンの軌跡を取得するシステムが同タイミングでデータを取得できるようにして, ブラウザ上のものとカメラ画像のものとでずれがどれくらいあるかを検証する予定です.

軌跡を取得し始めるタイミング -> pointerdown
軌跡を取得するイベント -> pointer move
軌跡の取得をやめるタイミング -> pointerup

p5.jsを自分の環境で使う
キャンバスの背景変更
カメラと連動

・スマホからペン先を指定する方法の考案
・軌跡の描画を切り替えるボタン
・スマートフォンから動かす
・書いたものの消去、保存

https://universe.roboflow.com/kitech-tqjyb/pen-detect-ngsot
@misc{
                            pen-detect-ngsot_dataset,
                            title = { Pen detect Dataset },
                            type = { Open Source Dataset },
                            author = { KITECH },
                            howpublished = { \url{ https://universe.roboflow.com/kitech-tqjyb/pen-detect-ngsot } },
                            url = { https://universe.roboflow.com/kitech-tqjyb/pen-detect-ngsot },
                            journal = { Roboflow Universe },
                            publisher = { Roboflow },
                            year = { 2023 },
                            month = { nov },
                            note = { visited on 2025-05-16 },
                            }