import keras
import shap
import numpy as np
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from utils.dataset import MnistDataset
import test_dnnct_tnn
import time
import pandas as pd
import concurrent.futures
import os
from multiprocessing import Process, Queue



def run_tnn_shap_test(idxs):
    df=pd.read_csv('shap/shap_values.csv')
    for idx in idxs:
        rows,cols=df['row'][idx],df['col'][idx]
        rows = rows.replace('[', '').replace(']', '')
        rows = [int(i) for i in rows.split(',')]
        cols = cols.replace('[', '').replace(']', '')
        cols = [int(i) for i in cols.split(',')]
        start_time = time.time()
        result = []  
        idx_tnn_count=0
        for i in range(8):
            tnn_results_df = pd.DataFrame(columns=['Iteration','TNN_Count'])
            tnn_count=0
            tnn_count=tnn_count+test_dnnct_tnn.shap_pixel_test(i, idx, rows, cols)
            idx_tnn_count=idx_tnn_count+tnn_count
            tnn_results_df.loc[i] = [i+1,idx_tnn_count]
            result.append(tnn_results_df)  # Append the DataFrame to the list
        total_time = time.time() - start_time
        file_path=f'out/tnn_delta/'
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        with open(f'{file_path}/tnn_shap_time_{idx}_{i}', 'w') as file:
            file.write('Total execution time: {} seconds'.format(total_time))
        final_df = pd.concat(result)  # Concatenate all DataFrame objects in the list
        final_df.to_csv(f'out/tnn_delta/df/tnn_shap_results_{idx}.csv', index=False)
        # final_df.to_csv(f'out/tnn/df/tnn_shap_results_{idx}.csv', index=False)




def run_tnn_shap_timeout_test(idxs):
    df=pd.read_csv('shap/shap_values.csv')
    for idx in idxs:
        rows,cols=df['row'][idx],df['col'][idx]
        rows = rows.replace('[', '').replace(']', '')
        rows = [int(i) for i in rows.split(',')]
        cols = cols.replace('[', '').replace(']', '')
        cols = [int(i) for i in cols.split(',')]
        start_time = time.time()
        result = []  
        timeout = 100
        tnn_count=0
        for i in [0, 1, 3, 7, 15]:
            tnn_results_df = pd.DataFrame(columns=['Iteration','TNN_Count'])
            try:
                recorder=test_dnnct_tnn.shap_pixel_timeout_test(i, idx, rows, cols, timeout)
                if recorder.attack_label!=None:
                   tnn_count=1
                   tnn_results_df.loc[i] = [i, tnn_count]
                   result.append(tnn_results_df)
                   break
            except Exception as err:
                print(f"Unexpected {err=}, {type(err)=}")
                raise
            tnn_results_df.loc[i] = [i, tnn_count]
            timeout += 100
            result.append(tnn_results_df)  # Append the DataFrame to the list
        total_time = time.time() - start_time
        file_path=f'out/tnn_timeout/'
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        with open(f'{file_path}/tnn_shap_time_{idx}_{i}', 'w') as file:
            file.write('Total execution time: {} seconds'.format(total_time))
        final_df = pd.concat(result)  # Concatenate all DataFrame objects in the list
        final_df.to_csv(f'{file_path}/df/tnn_shap_results_{idx}.csv', index=False)


if __name__ == "__main__":

    # var1=330
    var1=35
    processes = []
    max_processes = 5
    all_subprocess_tasks = [[] for _ in range(max_processes)]
    cursor = 0
    for i in range(var1,var1+1):
        all_subprocess_tasks[cursor].append(i)
        cursor+=1
        if cursor == max_processes:
            cursor = 0
    running_processes = []
    
    for sub_tasks in all_subprocess_tasks:
            if len(sub_tasks) > 0:
                p = Process(target=run_tnn_shap_test, args=(sub_tasks,))
                p.start()
                # p.daemon=True
                running_processes.append(p)

                time.sleep(1) 

    for p in running_processes:
            p.join()















