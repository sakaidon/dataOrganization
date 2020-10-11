import glob
import pandas as pd

# 同一ディレクトリ内のtxtファイル名リスト取得
fileNames = glob.glob("*.txt")
fileNames.sort()
matome = []

# 各ファイルデータ取得
for i in range(len(fileNames)):
    file_data = open(fileNames[i], "r") # ファイルオープン
    
# 一つ目のファイルのみWavelengthの値も取得
    if i == 0:
        matome.append(["Wavelength",fileNames[i][:-4]])
        for line in file_data:
            tmp = line.split(";")
            if len(tmp) > 13 and tmp[1] != "Wavelength" and tmp[1] != '   ':
                matome.append([tmp[1], tmp[7]])

# 二つ目以降のファイルのデータ取得
    else:
        cnt =1
        matome[0].append(fileNames[i][:-4])
        for line in file_data:
            tmp = line.split(";")
            if len(tmp) > 13 and tmp[1] != "Wavelength" and tmp[1] != '   ':
                matome[cnt].append(tmp[7])
                cnt += 1
                
    file_data.close() # ファイルクローズ
    
# csv形式で出力
df = pd.DataFrame(matome)
df.to_csv("matome.csv")