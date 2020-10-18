import math
import glob
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# import scipy
MIN_AMP = 0.23 # min_amp以下のamplitudeを持つ周波数をカット


# ノイズ除去処理
def my_lowpath(x, y, min_amp):
    N = len(x)
    dt = x[1] - x[0]
    yf = np.fft.fft(y)
    freq = np.linspace(0, 1.0/dt, N)
    yf_abs = np.abs(yf)
    yf_abs_amp = yf_abs/N * 2
    yf_abs_amp[0] = yf_abs_amp[0]/2
    amp2 = yf.copy()
    amp2[(yf_abs_amp < min_amp)] = 0
    y2 = np.fft.ifft(amp2).real
    amp2 = np.abs(amp2)/N * 2
    amp2[0] /= 2
    return y2


# 同一ディレクトリ内のtxtファイル名リスト取得
fileNames = glob.glob("*.txt")
fileNames.sort()
table = []


# 各ファイルデータ取得
for i in range(len(fileNames)):
    file_data = open(fileNames[i], "r") # ファイルオープン
    

    # 1つ目のファイルのみx軸のデータも記録
    if i == 0:
        cnt = 0
        tmp_x = []
        tmp_y = []
        table.append(["Time (ns)", fileNames[0][:-4], "lowpathed_{fileName}".format(fileName=fileNames[0][:-4])])

        for line in file_data:
            tmp = line.replace("\n","").split("  ")
            if cnt >= 10 and cnt < 3000 and len(tmp) == 3:
                table.append([float(tmp[0]), int(tmp[2])])
                tmp_x.append(float(tmp[0]))
                tmp_y.append(int(tmp[2]))
            cnt += 1

        tmp_after_y = my_lowpath(tmp_x, tmp_y, MIN_AMP)
        for j in range(len(tmp_x)):
            table[j + 1].append(tmp_after_y[j])


    # 2つめ以降のファイル
    else:
        cnt = 0
        now = 1
        tmp_x = []
        tmp_y = []
        table[0].append(fileNames[i][:-4])
        table[0].append("lowpathed_{fileName}".format(fileName=fileNames[i][:-4]))

        for line in file_data:
            tmp = line.replace("\n","").split("  ")
            if cnt >= 10 and cnt < 3000 and len(tmp) == 3:
                table[now].append(int(tmp[2]))
                tmp_x.append(float(tmp[0]))
                tmp_y.append(int(tmp[2]))
                now += 1
            cnt += 1

        tmp_after_y = my_lowpath(tmp_x, tmp_y, MIN_AMP)
        for j in range(len(tmp_x)):
            table[j + 1].append(tmp_after_y[j])


    file_data.close() # ファイルクローズ


# csv形式で出力
df = pd.DataFrame(table)
df.to_csv("matome.csv")

# fig = plt.figure()
# ax = fig.add_subplot(111, title='Raw data', ylabel='count', xlabel='Time (ns)')
# line = ax.plot(x, y)
# fig.savefig("img.png")

# fig = plt.figure()
# ax = fig.add_subplot(111, title='FFT', ylabel='freq (GHz)', xlabel='Amplitude')
# line = ax.plot(freq, yf_abs_amp)
# fig.savefig("img2.png")

# fig = plt.figure()
# ax = fig.add_subplot(111, title='FFT (noise Removed)', ylabel='freq (GHz)', xlabel='Amplitude')
# line = ax.plot(freq, amp2)
# fig.savefig("img3.png")

# fig = plt.figure()
# ax = fig.add_subplot(111, title='Low-path data', ylabel='count', xlabel='time (ns)')
# line = ax.plot(x, y2)
# fig.savefig("img4.png")