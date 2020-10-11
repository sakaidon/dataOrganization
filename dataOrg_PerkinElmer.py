import glob
import re
import pandas as pd

# 同一ディレクトリ内のtxtファイル名リスト取得
fileNames = glob.glob("*.txt")
fileNames.sort()
matome = []

# 各ファイルデータ取得
for i in range(len(fileNames)):
    file_data = open(fileNames[i], "r") # ファイルオープン

    no_data = True #必要な部分かどうか判定
    
# 一つ目のファイルのみWavelengthの値も取得
    if i == 0:
        matome.append(["Wavelength",fileNames[i][:-4]])
        for line in file_data:
            tmp = re.split('[\t ]', line)
            print(tmp)
            if tmp[0] == "#DATA\n":
                print (1)
                no_data = False
                continue
            if len(tmp) < 2:
                continue
            if not no_data:
                matome.append([tmp[0], tmp[1]])

# 二つ目以降のファイルのデータ取得
    else:
        cnt =1
        matome[0].append(fileNames[i][:-4])
        for line in file_data:
            tmp = re.split('[\t ]', line)
            if tmp[0] == "#DATA\n":
                no_data = False
                continue
            if len(tmp) < 2:
                continue
            if not no_data:
                matome[cnt].append(tmp[1])
                cnt += 1
                
    file_data.close() # ファイルクローズ
    
# csv形式で出力
df = pd.DataFrame(matome)
df.to_csv("matome.csv")