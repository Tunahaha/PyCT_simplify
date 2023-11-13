import time
import os


# 您的 Python 檔案的路徑
filepath = "run_shap.py"


# 您想要修改的變數
variable = "var1"


# 您想要修改變數的頻率（以秒為單位）
# 半小時等於 1800 秒
frequency = 3600


# 您想要輸入的數字
numbers = list(range(0, 1001, 20))
index = 0


while True:
    # 讀取文件內容
    with open(filepath, "r") as f:
        lines = f.readlines()


    # 修改變數的值
    for i, line in enumerate(lines):
        if line.strip().startswith(variable):
            lines[i] = f"{variable} = {numbers[index]}\n"
            break


    # 寫回文件
    with open(filepath, "w") as f:
        f.writelines(lines)


    # 在終端中運行 Python 檔案
    os.system(f"python {filepath}")


    index = (index + 1) % len(numbers)


    # 等待一段時間
    time.sleep(frequency)




