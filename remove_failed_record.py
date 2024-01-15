#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import json
from tqdm import tqdm
from pathlib import Path
import shutil

# remove_dir = './exp/'
remove_dir = './exp/mnist_sep_act_m7_9876/'
input_name = 'mnist_test_'
error_count = 0

for record_dir in tqdm(Path(remove_dir).rglob(f'{input_name}*')):
    json_path = os.path.join(record_dir, "stats.json")
    has_json = os.path.exists(json_path)
    
    open_failed_json = False
    normal_finish = False
    with open(json_path) as f:
        try:
            stats = json.load(f)
            normal_finish = stats['meta']['is_finish']
        except json.JSONDecodeError as je:
            open_failed_json = True
            print(json_path, ":該筆紀錄壞掉")
    
    
    if not has_json or not normal_finish or open_failed_json:
        error_count += 1
        print('error record:', record_dir)
        # shutil.rmtree(record_dir)
        
print(f'total error count and removed: {error_count}')


# In[ ]:




