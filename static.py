import pandas as pd
import os
import re

def count_example():
    counts = {}
    for filename in os.listdir('out/tnn/df'):
        if filename.endswith('.csv'):
            # 讀取CSV檔案
            df = pd.read_csv(os.path.join('out/tnn/df', filename))
            
            # 遍歷每一行
            for index, row in df.iterrows():
                # 如果CNN_Count不為0
                if row['TNN_Count'] != 0:
                    # 將對應的Iteration的計數增加1
                    if row['Iteration'] in counts:
                        counts[row['Iteration']] += 1
                    else:
                        counts[row['Iteration']] = 1
    for key in sorted(counts.keys()):
        print('count_{}: {}'.format(key, counts[key]))


def count_size(directory):
    total = 0
    count = 0
    last_in_iteration = {}
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('constraint_size.txt'):
                # 讀取TXT檔案
                with open(os.path.join(root, filename), 'r') as f:
                    # 遍歷每一行
                    for line in f:
                        # 使用正規表達式找出數字
                        numbers = re.findall(r'[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?', line)
                        if numbers:
                            # 更新總數和數量
                            total += float(numbers[-1])
                            count += 1
                            # 更新該Iteration的最後一個數字
                            iteration = int(numbers[0])
                            last_in_iteration[iteration] = float(numbers[-1])
    # 計算平均值
    average = total / count if count > 0 else 0
    # 計算每個Iteration最後一個數字的平均值
    average_last = sum(last_in_iteration.values()) / len(last_in_iteration) if len(last_in_iteration) > 0 else 0

    print('Average size of the constraint: {} MB'.format(average))
    print('Average of the last number in each iteration: {} MB'.format(average_last))

def count_time(directory):
    # 初始化變數來追蹤總數和數量
    total = 0
    count = 0

    # 初始化字典來追蹤每個Iteration的最後一個數字
    last_in_iteration = {}


    # 遍歷資料夾及其子資料夾中的所有TXT檔案
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('constraint_time.txt'):
                # 讀取TXT檔案
                with open(os.path.join(root, filename), 'r') as f:
                    # 遍歷每一行
                    for line in f:
                        # 使用正規表達式找出數字
                        numbers = re.findall(r'[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?', line)
                        if numbers:
                            # 更新總數和數量
                            total += float(numbers[-1])
                            count += 1
                            # 更新該Iteration的最後一個數字
                            iteration = int(numbers[0])
                            last_in_iteration[iteration] = float(numbers[-1])


    # 計算平均值
    average = total / count if count > 0 else 0


    # 計算每個Iteration最後一個數字的平均值
    average_last = sum(last_in_iteration.values()) / len(last_in_iteration) if len(last_in_iteration) > 0 else 0
    print('Average time of the constraint: {} seconds'.format(average))
    print('Average of the last number in each iteration: {} seconds'.format(average_last))
def count_smt2(directory):
    # 初始化變數來追蹤smt2檔案數量
    count = 0


    # 遍歷資料夾及其子資料夾中的所有檔案
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.smt2'):
                # 如果檔案是smt2檔案，則增加計數
                count += 1


    print('Number of smt2 files: {}'.format(count))

def avg_sat_smt2(directory):
    # 初始化變數來追蹤smt2檔案數量和資料夾數量
    file_count = 0
    dir_count = 0
    for root, dirs, files in os.walk(directory):
        smt2_in_current_dir = sum(filename.endswith('_sat.smt2') for filename in files)
        if smt2_in_current_dir > 0:
            # 如果當前資料夾中有smt2檔案，則增加檔案計數和資料夾計數
            file_count += smt2_in_current_dir
            dir_count += 1

    average = file_count / dir_count if dir_count > 0 else 0
    print('Average number of smt2 files per directory: {}'.format(average))







# 呼叫函數
#count_size('exp/mnist_sep_act_m6_9628/queue/test_tnn/test_3_pixel_forward')
# count_smt2('exp/mnist_sep_act_m6_9628/queue/test_cnn/test_0_pixel_forward')
# count_smt2('exp/mnist_sep_act_m6_9628/queue/test_cnn/test_1_pixel_forward')
# count_smt2('exp/mnist_sep_act_m6_9628/queue/test_cnn/test_2_pixel_forward')
# count_smt2('exp/mnist_sep_act_m6_9628/queue/test_cnn/test_3_pixel_forward')
# count_smt2('exp/mnist_sep_act_m6_9628/queue/test_cnn/test_4_pixel_forward')
# count_smt2('exp/mnist_sep_act_m6_9628/queue/test_cnn/test_5_pixel_forward')
# count_smt2('exp/mnist_sep_act_m6_9628/queue/test_cnn/test_6_pixel_forward')
# count_smt2('exp/mnist_sep_act_m6_9628/queue/test_cnn/test_7_pixel_forward')

def avg_smt2(directory):
    # 初始化變數來追蹤smt2檔案數量和資料夾數量
    file_count = 0
    dir_count = 0


    # 遍歷資料夾及其子資料夾中的所有檔案
    for root, dirs, files in os.walk(directory):
        smt2_in_current_dir = sum(filename.endswith('.smt2') for filename in files)
        if smt2_in_current_dir > 0:
            # 如果當前資料夾中有smt2檔案，則增加檔案計數和資料夾計數
            file_count += smt2_in_current_dir
            dir_count += 1


    # 計算平均值
    average = file_count / dir_count if dir_count > 0 else 0


    print('Average number of smt2 files per directory: {}'.format(average))

def count_5rd_size(directory):
    # 初始化變數來追蹤總數和數量
    total = 0
    count = 0
    # 遍歷資料夾及其子資料夾中的所有TXT檔案
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('constraint_size.txt'):
                # 讀取TXT檔案
                with open(os.path.join(root, filename), 'r') as f:
                    # 遍歷前五行
                    for i, line in enumerate(f):
                        if i < 5:
                            # 使用正規表達式找出數字
                            numbers = re.findall(r'[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?', line)
                            if numbers:
                                # 更新總數和數量
                                total += float(numbers[-1])
                                count += 1
    average = total / count if count > 0 else 0
    print('Average of the last number in first 5 lines: {} MB'.format(average))

def count_1rd_size(directory):
    # 初始化變數來追蹤總數和數量
    total = 0
    count = 0
    # 遍歷資料夾及其子資料夾中的所有TXT檔案
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('constraint_size.txt'):
                # 讀取TXT檔案
                with open(os.path.join(root, filename), 'r') as f:
                    # 遍歷前五行
                    for i, line in enumerate(f):
                        if i < 1:
                            # 使用正規表達式找出數字
                            numbers = re.findall(r'[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?', line)
                            if numbers:
                                # 更新總數和數量
                                total += float(numbers[-1])
                                count += 1
    average = total / count if count > 0 else 0
    print('Average of the last number in first 5 lines: {} MB'.format(average))
def count_3rd_size(directory):
    # 初始化變數來追蹤總數和數量
    total = 0
    count = 0
    # 遍歷資料夾及其子資料夾中的所有TXT檔案
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('constraint_size.txt'):
                # 讀取TXT檔案
                with open(os.path.join(root, filename), 'r') as f:
                    # 遍歷前五行
                    for i, line in enumerate(f):
                        if i < 3:
                            # 使用正規表達式找出數字
                            numbers = re.findall(r'[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?', line)
                            if numbers:
                                # 更新總數和數量
                                total += float(numbers[-1])
                                count += 1
    average = total / count if count > 0 else 0
    print('Average of the last number in first 5 lines: {} MB'.format(average))





# count_1rd_size('exp/mnist_sep_act_m6_9628/queue/test_cnn/test_0_pixel_forward')
# count_1rd_size('exp/mnist_sep_act_m6_9628/queue/test_cnn/test_1_pixel_forward')
# count_1rd_size('exp/mnist_sep_act_m6_9628/queue/test_cnn/test_2_pixel_forward')
# count_1rd_size('exp/mnist_sep_act_m6_9628/queue/test_cnn/test_3_pixel_forward')
# count_1rd_size('exp/mnist_sep_act_m6_9628/queue/test_cnn/test_4_pixel_forward')
# count_1rd_size('exp/mnist_sep_act_m6_9628/queue/test_cnn/test_5_pixel_forward')
# count_1rd_size('exp/mnist_sep_act_m6_9628/queue/test_cnn/test_6_pixel_forward')
# count_1rd_size('exp/mnist_sep_act_m6_9628/queue/test_cnn/test_7_pixel_forward')
from keras.models import load_model

# 載入模型
model = load_model('model/mnist_sep_act_m6_9628.h5')

# 查看模型架構和參數數量
model.summary()




