import time
from multiprocessing import Process


NUM_PROCESS = 1
TIMEOUT = 3600
NORM_01 = False
model_name = "paper_example_RNN"

def create_and_save_paper_example_RNN_model():
    import numpy as np
    import keras
    from keras import layers
    model = keras.models.Sequential()
    model.add(layers.SimpleRNN(2, activation=None, input_shape=(2, 2)))

    w_xh = [
        [0.1, 0.02],
        [0.3, 0.5],
    ]
    w_hh = [
        [1, 0.1],
        [2, 0.2],
    ]
    b_h = [0.2, 0.1]
    w_xh = np.array(w_xh)
    w_hh = np.array(w_hh)
    b_h = np.array(b_h)
    weights = [w_xh, w_hh, b_h]

    model.layers[0].set_weights(weights)
    model.layers[0].weights

    model.save(f"model/{model_name}.h5")
    

if __name__ == "__main__":
    from utils.pyct_attack_exp import run_multi_attack_subprocess_wall_timeout
    from utils.pyct_attack_exp_research_question import paper_example_RNN_fake_data
    
    create_and_save_paper_example_RNN_model()
    

    inputs = paper_example_RNN_fake_data(model_name)
    

    print("#"*40, f"number of inputs: {len(inputs)}", "#"*40)
    time.sleep(3)

    ########## 分派input給各個subprocesses ##########    
    all_subprocess_tasks = [[] for _ in range(NUM_PROCESS)]
    cursor = 0
    for task in inputs:    
        all_subprocess_tasks[cursor].append(task)    
       
        cursor+=1
        if cursor == NUM_PROCESS:
            cursor = 0


    running_processes = []
    for sub_tasks in all_subprocess_tasks:
        if len(sub_tasks) > 0:
            p = Process(target=run_multi_attack_subprocess_wall_timeout, args=(sub_tasks, TIMEOUT, NORM_01,))
            p.start()
            running_processes.append(p)
            time.sleep(1) # subprocess start 的間隔時間
       
    for p in running_processes:
        p.join()

    print('done')
