import cv2
import numpy as np
# import openpyxl

# import test_svm

# Esc キー
ESC_KEY = 0x1b
# s キー
S_KEY = 0x73
# dキー
D_KEY = 0x64
# r キー
R_KEY = 0x72
# 特徴点の最大数
MAX_FEATURE_NUM = 1
# 反復アルゴリズムの終了条件
CRITERIA = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03)
# インターバル （1000 / フレームレート）
INTERVAL = 30
# ビデオデータ
# VIDEO_DATA = 'testvideo/new_a.mp4'
# VIDEO_DATA = 1
# Excelファイル
# file_name = 'excel/ipsj_o.xlsx'
# WORKBOOK = openpyxl.load_workbook(file_name)
# sheet = WORKBOOK['Sheet5']
# データ格納用リスト
datalist = []
pointlist=[]
labellist=[]
idx = -1
# 距離格納用
far_val = None
class Motion:
    # コンストラクタ
    def __init__(self):
        # 表示ウィンドウ
        cv2.namedWindow("motion")
        # マウスイベントのコールバック登録
        cv2.setMouseCallback("motion", self.onMouse)
        # 映像
        # self.video = cv2.VideoCapture(VIDEO_DATA)
        self.video = cv2.VideoCapture(0)

        # インターバル
        self.interval = INTERVAL
        # 現在のフレーム（カラー）
        self.frame = None
        # 現在のフレーム（グレー）
        self.gray_next = None
        # 前回のフレーム（グレー）
        self.gray_prev = None
        # 特徴点
        self.features = None
        # 特徴点のステータス
        self.status = None
        # 特徴点の軌跡描画用マスク
        self.mask = None
        # predict用関数
        self.count = 0
        self.start = 0
        #drawflag
        self.drawflag = False
        # 値保持用配列
        self.fea = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]
        # self.temp = None
        # self.proba = None

    # メインループ
    def run(self):
        global datalist, idx, sheet, WORKBOOK
        # 最初のフレームの処理
        # videoが正常に読み込めた場合, end_flag には true, self.frameにはビデオフレーム?が入る
        end_flag, self.frame = self.video.read()
        # フレームの大きさを調整する
        self.frame = cv2.resize(self.frame, dsize=None, fx=1.5, fy=1.5)
        # グレースケール変換(オプティカルフローに使うフレーム(前))
        self.gray_prev = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)

        self.mask = np.zeros_like(self.frame)

        while end_flag:
            # グレースケールに変換
            self.gray_next = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)

            # 特徴点が登録されている場合にOpticalFlowを計算する
            if self.features is not None:
                # print(self.features)ss
                if len(pointlist) == 0:
                    pointlist.append([self.features[0][0][0], self.features[0][0][1]])
                # オプティカルフローの計算
                features_prev = self.features
                self.features, self.status, err = cv2.calcOpticalFlowPyrLK( \
                                                    self.gray_prev, \
                                                    self.gray_next, \
                                                    features_prev, \
                                                    None, \
                                                    winSize = (30, 30), \
                                                    maxLevel = 3, \
                                                    criteria = CRITERIA, \
                                                    flags = 0)
                # calcOpticalFlowPyrLKは引数として(前のフレーム, 後のフレーム, 前の特徴点, 後の特徴点, ウィンドウサイズ, maxLevel, criteria, flags)を取る


                # 有効な特徴点のみ残す
                self.refreshFeatures()

                # フレームに有効な特徴点を描画
                if self.features is not None:
                    for feature in self.features:
                        cv2.circle(self.frame, (int(feature[0][0]), int(feature[0][1])), 2, (15, 241, 255), -1, 8, 0)
                        # self.mask = cv2.circle(self.mask, (int(feature[0][0]), int(feature[0][1])), 2, (15, 241, 255), -1, 8, 0)
                        self.fea.pop(0)
                        self.fea.append([feature[0][0], feature[0][1]])
                        pointlist.append([feature[0][0], feature[0][1]])
                        # print([feature[0][0], feature[0][1]])
                        
                
                # 特徴点の軌跡を描画
                if features_prev is not None:
                    for prev_feature in features_prev:
                        for feature in self.features:
                            p = np.array([prev_feature[0][0], prev_feature[0][1]])
                            q = np.array([feature[0][0], feature[0][1]])
                            # print(p, q)
                            if self.count == 23 or self.count == 41 or self.count == 61 or self.count == 90 or self.count == 103 or self.count == 162:
                                # print(self.count == 23 or self.count == 41 or self.count == 61 or self.count == 90 or self.count == 162)
                                self.drawflag = not self.drawflag
                            if self.drawflag:
                                self.mask = cv2.line(self.mask, (int(prev_feature[0][0]), int(prev_feature[0][1])), (int(feature[0][0]), int(feature[0][1])), (68, 114, 196), 2, 8, 0)
                            else:
                                self.mask = cv2.line(self.mask, (int(prev_feature[0][0]), int(prev_feature[0][1])), (int(feature[0][0]), int(feature[0][1])), (237, 125, 49), 2, 8, 0)
                            # 前フレームとの特徴点の距離で接触判定を行うため,　距離を計算して変数に格納する
                            dist = np.linalg.norm(p - q)
                            # print(dist)
                            datalist.append(dist)
                            self.count += 1
                            idx += 1

                # temp = self.predict2()
                # print(temp)
                # proba = self.predict()
                # print(proba)
                # print(self.fea)
                # if temp[1] > 0.5:
                    # if proba[temp] < 70:
                    #     break
                    # labellist.append(1)
                    # self.mask = cv2.line(self.mask, (int(self.fea[1][0]), int(self.fea[1][1])), (int(self.fea[2][0]), int(self.fea[2][1])), (15, 241, 255), 2, 8, 0)
                    # print("complete")
                # elif proba[temp] < 70:
                #     self.mask = cv2.line(self.mask, (int(self.fea[0][0]), int(self.fea[0][1])), (int(self.fea[1][0]), int(self.fea[1][1])), (15, 241, 255), 2, 8, 0)
                # elif self.count >= 5:
                #     self.mask = cv2.line(self.mask, (int(self.fea[1][0]), int(self.fea[1][1])), (int(self.fea[2][0]), int(self.fea[2][1])), (127, 255, 0), 1, 8, 0)
                # else:
                    # labellist.append(0)

            img = cv2.add(self.frame, self.mask)
            # 表示
            cv2.imshow("motion", img)

            # 次のループ処理の準備
            self.gray_prev = self.gray_next
            end_flag, self.frame = self.video.read()
            if end_flag:
                self.frame = cv2.resize(self.frame, dsize=None, fx=1.5, fy=1.5)
                self.gray_next = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)

            # インターバル
            key = cv2.waitKey(self.interval)
            # "Esc"キー押下で終了
            if key == ESC_KEY:
                break
            # "s"キー押下で一時停止
            elif key == S_KEY:
                self.interval = 0
            elif key == D_KEY:
                self.interval = 0
                print("dist: {} index: {}".format(datalist[idx], idx))
            elif key == R_KEY:
                self.interval = INTERVAL

        #Excelに書く
        # for i in range(len(datalist)):
        #     sheet.cell(row=i+1, column=1, value=pointlist[i][0])
        #     sheet.cell(row=i+1, column=2, value=pointlist[i][1])
        #     sheet.cell(row=i+1, column=3, value=datalist[i])
        #     if i == 0:
        #         sheet.cell(row=i+1, column=4, value=0)
        #         sheet.cell(row=i+1, column=5, value=0)
        #     else:
        #         sheet.cell(row=i+1, column=4, value=(pointlist[i][0]-pointlist[i-1][0]))
        #         sheet.cell(row=i+1, column=5, value=(pointlist[i][1]-pointlist[i-1][1]))
        # WORKBOOK.save(file_name)
        # 終了処理
        cv2.destroyAllWindows()
        self.video.release()


    # マウスクリックで特徴点を指定する
    #     クリックされた近傍に既存の特徴点がある場合は既存の特徴点を削除する
    #     クリックされた近傍に既存の特徴点がない場合は新規に特徴点を追加する
    def onMouse(self, event, x, y, flags, param):
        # 左クリック以外
        if event != cv2.EVENT_LBUTTONDOWN:
            return

        # 最初の特徴点追加
        if self.features is None:
            self.addFeature(x, y)
            # if len(pointlist) == 0:
            #         pointlist.append(x, y)
            return

        # 探索半径（pixel）
        radius = 5
        # 既存の特徴点が近傍にあるか探索
        index = self.getFeatureIndex(x, y, radius)

        # クリックされた近傍に既存の特徴点があるので既存の特徴点を削除する
        if index >= 0:
            self.features = np.delete(self.features, index, 0)
            self.status = np.delete(self.status, index, 0)

        # クリックされた近傍に既存の特徴点がないので新規に特徴点を追加する
        else:
            self.addFeature(x, y)

        return


    # 指定した半径内にある既存の特徴点のインデックスを１つ取得する
    #     指定した半径内に特徴点がない場合 index = -1 を応答
    def getFeatureIndex(self, x, y, radius):
        index = -1

        # 特徴点が１つも登録されていない
        if self.features is None:
            return index

        max_r2 = radius ** 2
        index = 0
        for point in self.features:
            dx = x - point[0][0]
            dy = y - point[0][1]
            r2 = dx ** 2 + dy ** 2
            if r2 <= max_r2:
                # この特徴点は指定された半径内
                return index
            else:
                # この特徴点は指定された半径外
                index += 1

        # 全ての特徴点が指定された半径の外側にある
        return -1


    # 特徴点を新規に追加する
    def addFeature(self, x, y):

        # 特徴点が未登録
        if self.features is None:
            # ndarrayの作成し特徴点の座標を登録
            self.features = np.array([[[x, y]]], np.float32)
            self.status = np.array([1])
            # 特徴点を高精度化
            cv2.cornerSubPix(self.gray_next, self.features, (10, 10), (-1, -1), CRITERIA)

        # 特徴点の最大登録個数をオーバー
        elif len(self.features) >= MAX_FEATURE_NUM:
            print("max feature num over: " + str(MAX_FEATURE_NUM))

        # 特徴点を追加登録
        else:
            # 既存のndarrayの最後に特徴点の座標を追加
            self.features = np.append(self.features, [[[x, y]]], axis = 0).astype(np.float32)
            self.status = np.append(self.status, 1)
            # 特徴点を高精度化
            cv2.cornerSubPix(self.gray_next, self.features, (10, 10), (-1, -1), CRITERIA)


    # 有効な特徴点のみ残す
    def refreshFeatures(self):
        # 特徴点が未登録
        if self.features is None:
            return

        # 全statusをチェックする
        i = 0
        while i < len(self.features):

            # 特徴点として認識できず
            if self.status[i] == 0:
                # 既存のndarrayから削除
                self.features = np.delete(self.features, i, 0)
                self.status = np.delete(self.status, i, 0)
                i -= 1

            i += 1

    # def predict(self):
    #     if self.count < 5:
    #         return [0, 0]
        
    #     templist = datalist[self.start:self.count]
    #     val1 = templist[0] - templist[2]
    #     val2 = templist[1] - templist[2]
    #     val3 = templist[2] - templist[3]
    #     val4 = templist[2] - templist[4]
    #     vallist = [templist[2], val1, val2, val3, val4]
    #     print(vallist)
    #     ret = test_svm.clf.predict([vallist])
    #     proba = test_svm.clf.predict_proba([vallist])
    #     # print(proba[0])
    #     print(ret)
    #     self.start += 1
    #     # theta = self.calctheta()
    #     # print([theta, ret])
    #     return proba[0]
    
    # def predict2(self):
    #     if len(pointlist) <= 1:
    #         return [0, 0]
        
    #     length = len(pointlist) - 1
    #     # print(length)
    #     prev_point_x = pointlist[length-1][0]
    #     prev_point_y = pointlist[length-1][1]
    #     point_x = pointlist[length][0]
    #     point_y = pointlist[length][1]

    #     p = np.array([prev_point_x, prev_point_y])
    #     q = np.array([point_x, point_y])
    #     dist = np.linalg.norm(p - q)

    #     dx = point_x - prev_point_x
    #     dy = point_y - prev_point_y

    #     vallist = [point_x, point_y, dist, dx, dy]
    #     print(vallist)
    #     ret = test_svm.clf.predict([vallist])
    #     print(ret)
    #     proba = test_svm.clf.predict_proba([vallist])
    #     return proba[0]



if __name__ == '__main__':
    Motion().run()
