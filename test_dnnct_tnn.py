#!/usr/bin/env python3

import argparse, logging, os, sys
import run_dnnct
import time
import numpy as np
from tensorflow.keras.models import load_model

from utils.dataset import MnistDataset
# Our main program starts now!
# f = argparse.RawTextHelpFormatter._split_lines
# argparse.RawTextHelpFormatter._split_lines = lambda *args, **kwargs: f(*args, **kwargs) + ['']
parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)

# positional arguments
parser.add_argument("modpath", metavar="path.to.module", help="import path to the target module (file) relative to the project root\nEx1: ./a/b/c.py -> a.b.c\nEx2: ./def.py -> def")
parser.add_argument("input", metavar="input_dict", help="dictionary of initial arguments to be passed into the target function\nPlease note that the double quotes enclosing the dictionary cannot be omitted!\nEx1: func(a=1,b=2) -> \"{'a':1,'b':2}\"\nEx2: func(a='',b='') -> \"{'a':'','b':''}\"\n\nIf a function parameter is not assigned in this dictionary, the program will first\ncheck if it has a type annotation. If it does, the program will use the corresponding\nconstructor as its default value. For example, int() returns 0 and str() returns an\nempty string. Otherwise the program continues to check if it provides a default value.\nIf it does, the default value will be used directly. Otherwise the program simply uses\nan empty string as its default value.")

# optional arguments
parser.add_argument("--dump_projstats", dest="dump_projstats", action='store_true', help="dump project statistics under the directory \"./project_statistics/{ProjectName}/{path.\nto.module}/{FUNC}/\"")
parser.add_argument("--file_as_total", dest="file_as_total", action='store_true', help="By default the program stops testing when the full coverage of this target function is\nachieved. If this option is enabled, the program stops testing when the full coverage\nof this target \"file\" is achieved instead.", default=False)
parser.add_argument("-d", "--formula", dest='formula', help="name of directory or file to store smtlib2 formulas\n(*) When this argument is a pure positive integer N, it means that we only want to\nstore the N_th constraint where N is the number \"SMT-id\" shown in the log. The file\nshould be named {N}.smt2 in the current directory.\n(*) Otherwise, this argument names the directory, and all constraints will be stored\nin this directory whose names follow the rule mentioned above.\nIn either case, these *.smt2 files should be able to be called by a solver directly.", default=None)
parser.add_argument("-s", "--func", dest="func", help="name of the target function\n(*) If the function {f} is standalone, this name is {f}.\n(*) If the function {f} belongs to a class {C}, this name should be {C.f}.\n(*) If the function name is the same as that of the target file, this option can be\nsimply omitted.", default=None)
parser.add_argument("--include_exception", dest="include_exception", action='store_true', help="also update coverage statistics when the iteration is terminated by a exception.")
parser.add_argument("-m", "--iter", dest="iter", help="maximum number of iterations [default = oo]", type=int, default=0)
parser.add_argument("--lib", dest="lib", help="another library path to be inserted at the beginning of sys.path\nFor example, if the target function resides in another folder requiring a virtual\nenvironment, you may want to do \"--lib {path-to-target-root}/.venv/lib/python3.8/site-\npackages\".", default=None)
parser.add_argument("-l", "--logfile", dest='logfile', help="path to the desired log file\n(*) When this argument is an empty string, all logging messages will not be dumped\neither to screens or to files.\n(*) When this option is not set, the logging messages will be dumped to screens.", default=None)
parser.add_argument("-r", "--root", dest="root", help="path to the project root which the target function resides in [default = path/to/this/\nproject]\nThe option should always be provided if the target function resides in another folder.", default=os.path.dirname(__file__))
parser.add_argument("--safety", dest="safety", help="indicates the behavior when the values in Python and in SMTLIB2 of a concolic object\nare not equal. [default = 0]\n(0) The symbolic expression is still preserved even if the values are different.\n(1) The symbolic expression is erased if the values are different, but the program\nstill continues.\n(2) The symbolic expression is erased if the values are different, and the program\nterminates soon.\nOnly in level 0 don't we verify the return value of the target function since some\nobjects in fact are not picklable, and therefore the return value is not printed in\nthe end.", type=int, default=0)
parser.add_argument("--single_timeout", dest="single_timeout", help="timeout (sec.) for the tester to go through one iteration [default = 15]", type=int, default=15)
parser.add_argument("-t", "--timeout", dest="timeout", help="timeout (sec.) for the solver to solve a constraint [default = 10]", type=int, default=10)
parser.add_argument("--total_timeout", dest="total_timeout", help="timeout (sec.) for the tester to go through all iterations [default = 900]", type=int, default=900)
parser.add_argument("-v", "--verbose", dest='verbose', help="logging level [default = 1]\n(0) Show messages whose levels not lower than WARNING.\n(1) Show messages from (0), plus basic iteration information.\n(2) Show messages from (1), plus solver information.\n(3) Show messages from (2), plus all concolic objects' information.", type=int, default=1)
parser.add_argument("-c", "--is_concolic", dest='concolic_dict', help="dictionary from argument name -> bool indicating if the argument has symbolic value. If not specified, the argument is default to be concolic.", type=str, default="")
parser.add_argument("-n", "--is_normalized", dest='norm', help="If normalize input to 0~1 (float type only) for DNN testing", type=bool, default=False)

# Solver configuration
# solver=[z3seq, z3str, trauc, cvc4]
# parser.add_argument("--solver", dest='solver', help="solver type [default = cvc4]\nWe currently only support CVC4.", default="cvc4")

# Parse arguments
# args = parser.parse_args()


##########################################

# model_name = "mnist_model48"
model_name = "mnist_sep_act_m6_9628"
if __name__ == "__main__":
    from utils.dataset import MnistDataset
    
    mnist_dataset = MnistDataset()

    ########################################
    # def test_solve_all_ctr():
    #     idx = 123
    #     in_dict, con_dict = mnist_dataset.get_mnist_test_data(idx=idx)
    #     con_dict["v_0_0_0"] = 1 # # 123 Cannot attack

    #     save_exp = {
    #         "input_name": f"mnist_test_{idx}",
    #         "exp_name": "test/random_1"
    #     }
        
    #     use_stack = False
    #     result = run_dnnct.run(
    #         model_name, in_dict, con_dict,
    #         save_exp=save_exp, norm=True, solve_order_stack=use_stack,
    #         max_iter=0, total_timeout=1800, single_timeout=1800, timeout=1800)
        
    #     recorder = result[1]
    #     assert recorder.solve_all_ctr
    # test_solve_all_ctr()

    # ########################################
    # # test timeout
    # def test_timeout():
    #     idx = 246
    #     in_dict, con_dict = mnist_dataset.get_mnist_test_data(idx=idx)
    #     con_dict["v_0_0_0"] = 1 # # 246 Cannot attack
    #     con_dict["v_9_27_0"] = 1 # # 246 Cannot attack
    #     con_dict["v_5_3_0"] = 1 # # 246 Cannot attack

    #     save_exp = {
    #         "input_name": f"mnist_test_{idx}",
    #         "exp_name": "test/random_3"
    #     }
    #     use_stack = False
    #     result = run_dnnct.run(
    #         model_name, in_dict, con_dict,
    #         save_exp=save_exp, norm=True, solve_order_stack=use_stack,
    #         max_iter=0, total_timeout=10, single_timeout=10, timeout=10)
        
    #     recorder = result[1]
    #     assert recorder.is_timeout
    # test_timeout()
    
    # ########################################
    # def test_queue_result():
    #     idx = 403
    #     in_dict, con_dict = mnist_dataset.get_mnist_test_data(idx=idx)
    #     con_dict["v_21_6_0"] = 1 # 403 # find solution fast

    #     save_exp = {
    #         "input_name": f"mnist_test_{idx}",
    #         "exp_name": "test/random_1"
    #     }
    #     use_stack = False
    #     result = run_dnnct.run(
    #         model_name, in_dict, con_dict,
    #         save_exp=save_exp, norm=True, solve_order_stack=use_stack,
    #         max_iter=0, total_timeout=1800, single_timeout=1800, timeout=1800)

    #     # check whether PyCT works properly when using queue
    #     recorder = result[1]
    #     assert recorder.total_iter == 1
    #     assert recorder.original_label == 8
    #     assert recorder.attack_label == 9
    #     assert recorder.sat == [0, 1]
    #     assert recorder.unsat == [0, 0]
    #     assert recorder.unknown == [0, 0]
    #     assert recorder.gen_constraint == [81, 100]
    #     assert recorder.solve_constraint == [0, 1]
    # test_queue_result()
    
    # ########################################
    # def test_stack_result():
    #     idx = 403
    #     in_dict, con_dict = mnist_dataset.get_mnist_test_data(idx=idx)
    #     con_dict["v_21_6_0"] = 1 # 403 # find solution slow

    #     save_exp = {
    #         "input_name": f"mnist_test_{idx}",
    #         "exp_name": "test/random_1"
    #     }
    #     use_stack = True
    #     result = run_dnnct.run(model_name, in_dict, con_dict, save_exp=save_exp, norm=True, solve_order_stack=use_stack,
    #                         max_iter=0, total_timeout=1800, single_timeout=1800, timeout=1800)

    #     # check whether PyCT works properly when using stack
    #     recorder = result[1]
    #     assert recorder.total_iter == 9
    #     assert recorder.original_label == 8
    #     assert recorder.attack_label == 9
    #     assert recorder.sat == [0,1,1,2,1,1,1,1,1,1]
    #     assert recorder.unsat == [0,62,62,56,6,29,29,58,58,92]
    #     assert recorder.unknown == [0,0,0,0,0,0,0,0,0,0]
    #     assert recorder.gen_constraint == [81,86,64,0,61,0,57,68,58,96]
    #     assert recorder.solve_constraint == [0,63,63,58,7,30,30,59,59,93]
    # test_stack_result()
    
    # def test_queue_result_limit():
    #     idx = 403
    #     in_dict, con_dict = mnist_dataset.get_mnist_test_data(idx=idx)
    #     con_dict["v_21_6_0"] = 1 # 403 # find solution fast

    #     save_exp = {
    #         "input_name": f"mnist_test_{idx}",
    #         "exp_name": "test_limit/random_1"
    #     }
    #     use_stack = False
    #     result = run_dnnct.run(
    #         model_name, in_dict, con_dict,
    #         save_exp=save_exp, norm=True, solve_order_stack=use_stack,
    #         max_iter=0, total_timeout=1800, single_timeout=1800, timeout=1800,
    #         limit_change_range=10, 
    #     )

    #     # check whether PyCT works properly when using queue
    #     recorder = result[1]
    #     assert recorder.total_iter == 1
    #     assert recorder.original_label == 8
    #     assert recorder.attack_label == None
    # test_queue_result_limit()
    

    def test_queue_result_limit_many_pixels(idx,num):
        idx = idx
        in_dict, con_dict = mnist_dataset.get_mnist_test_data(idx=idx)

        # if no change limit can be attacked in 1 iteration
        # if set change limit to 100 cannot be attacked in 1 iteration
        # if set change limit to 110 can be attacked in 1 iteration
        con_dict[f"v_12_7_0"] = 1
        con_dict[f"v_11_7_0"] = 1
        con_dict[f"v_13_9_0"] = 1
        con_dict[f"v_13_10_0"] = 1
        con_dict[f"v_13_8_0"] = 1
        con_dict[f"v_9_8_0"] = 1
        con_dict[f"v_8_8_0"] = 1
        con_dict[f"v_8_20_0"] = 1
        con_dict[f"v_14_20_0"] = 1
        con_dict[f"v_14_14_0"] = 1
        con_dict[f"v_15_15_0"] = 1
        # total_elements=28*28
        # for i in range(0, total_elements, num):
        #     con_dict[f"v_{i//28}_{i%28}_0"] = 1
        save_exp = {
            "input_name": f"mnist_test_{idx}",
            "exp_name": "test_tnn/test_queue_result_limit_many_pixels"
            # ,"save_smt":True
        }
        use_stack = False
        start_time = time.time()
        result = run_dnnct.run(
            model_name, in_dict, con_dict,model_type='tnn',
            save_exp=save_exp, norm=True, solve_order_stack=use_stack,
            max_iter=0, total_timeout=3600, single_timeout=1800, timeout=1800,
            limit_change_range=110,
        )
        total_time = time.time() - start_time

        # check whether PyCT works properly when using queue
        recorder = result[1]
        # assert recorder.total_iter == 1
        # assert recorder.original_label == 1
        # assert recorder.attack_label == 8

        original_input = np.squeeze(mnist_dataset.get_origin_mnist_test_data(idx=idx))
        adversarial_input = np.squeeze(recorder.adversarial_input)
        diff_indices = np.where(original_input != adversarial_input)
        diff_pairs = list(zip(diff_indices[0], diff_indices[1]))

        with open('out/tnn/output_dict.txt', 'w') as file:
            file.write('original_input:\n{}'.format(np.array2string(original_input, separator=', ')))
            file.write('\nadversarial_input:\n{}'.format(np.array2string(adversarial_input, separator=', ')))
            file.write('\ndifference_indices:\n{}'.format(str(diff_pairs)))

    # for i in range(6):
    #     print(f'num of pixels : {i}')
    # for j in range(8,15):
    #     print(f'nums : {j}')
    #     if test_queue_result_limit_many_pixels(6,j):
    #         break

    test_queue_result_limit_many_pixels(0,8)


    
    def test_one_pixel_forward():
        idx = 6
        in_dict, con_dict = mnist_dataset.get_mnist_test_data(idx=idx)

        # if no change limit can be attacked in 1 iteration
        # if set change limit to 100 cannot be attacked in 1 iteration
        # if set change limit to 110 can be attacked in 1 iteration
        con_dict[f"v_12_7_0"] = 1


        save_exp = {
            "input_name": f"mnist_test_{idx}",
            "exp_name": f"test_tnn/test_one_pixel_forward/{idx}"
            # ,"save_smt":True
        }
        use_stack = False
        start_time = time.time()
        result = run_dnnct.run(
            model_name, in_dict, con_dict,model_type='tnn',
            save_exp=save_exp, norm=True, solve_order_stack=use_stack,
            max_iter=0, total_timeout=3600, single_timeout=1800, timeout=1800,
            limit_change_range=110,
        )
        
        total_time = time.time() - start_time
        with open('out/tnn/one_pixel_time_record.txt', 'w') as file:
            file.write('Total execution time: {} seconds'.format(total_time))

        # check whether PyCT works properly when using queue
        recorder = result[1]
        # assert recorder.total_iter == 1
        # assert recorder.original_label == 1
        # assert recorder.attack_label == 8

        original_input = np.squeeze(mnist_dataset.get_origin_mnist_test_data(idx=idx))
        adversarial_input = np.squeeze(recorder.adversarial_input)
        diff_indices = np.where(original_input != adversarial_input)
        diff_pairs = list(zip(diff_indices[0], diff_indices[1]))

        with open('out/tnn/one_pixel_output_dict.txt', 'w') as file:
            file.write('original_input:\n{}'.format(np.array2string(original_input, separator=', ')))
            file.write('\nadversarial_input:\n{}'.format(np.array2string(adversarial_input, separator=', ')))
            file.write('\ndifference_indices:\n{}'.format(str(diff_pairs)))

mnist_dataset = MnistDataset()
def check_origin_cnn_result(idx, original_input,adversarial_input):
    print('#'*15)
    idx=idx
    original_input = original_input.reshape((1, 28, 28, 1))
    adversarial_input = adversarial_input.reshape((1, 28, 28, 1))
    print(f'original label : {mnist_dataset.get_y_test(idx)}')
    print(f'original_input shape : {original_input.shape}')
    print(f'adversarial_input shape : {adversarial_input.shape}')
    cnn_model = load_model('model/'+model_name+'.h5')
    original_predictions = cnn_model.predict(original_input)
    original_predicted_class = np.argmax(original_predictions, axis=-1)
    print(f'original prediction : {original_predicted_class}')
    adversarial_predictions = cnn_model.predict(original_input)
    adversarial_predicted_class = np.argmax(adversarial_predictions, axis=-1)
    print(f'adversarial predictions : {adversarial_predicted_class}')
    print('#'*15)
    if original_predicted_class == adversarial_predicted_class:
        print('Failed to attack')
        return False
    else:
        print('Successfully attacked')
        with open('out/tnn/adversarial.txt', 'w') as file:
                file.write(f'idx:\n{idx}\n')
                file.write(f'adversarial_input:\n{np.array2string(adversarial_input, separator=", ")}\n')

        return True

def one_pixel_test(idx,pixels):
    idx = idx
    in_dict, con_dict = mnist_dataset.get_mnist_test_data(idx=idx)
    con_dict[pixels] = 1
    save_exp = {
        "input_name": f"mnist_test_{idx}",
        "exp_name": f"test_tnn/test_one_pixel_forward/{idx}"
        ,"save_smt":True
    }
    use_stack = False
    start_time = time.time()
    result = run_dnnct.run(
        model_name, in_dict, con_dict,model_type='tnn',
        save_exp=save_exp, norm=True, solve_order_stack=use_stack,
        max_iter=0, total_timeout=3600, single_timeout=1800, timeout=1800,
        limit_change_range=110,
    )
    
    total_time = time.time() - start_time
    with open('out/tnn/one_pixel_time_record.txt', 'w') as file:
        file.write('Total execution time: {} seconds'.format(total_time))
    recorder = result[1]
    original_input = np.squeeze(mnist_dataset.get_origin_mnist_test_data(idx=idx))
    adversarial_input = np.squeeze(recorder.adversarial_input)
    if adversarial_input.size <= 1:
        return 0
    if check_origin_cnn_result(idx,original_input,adversarial_input):
        return 1
    else:
        return 0
def eight_pixel_test(num,idx,pixels):
    idx = idx
    in_dict, con_dict = mnist_dataset.get_mnist_test_data(idx=idx)

    for i in pixels:
        con_dict[i]=1
    save_exp = {
        "input_name": f"mnist_test_{idx}",
        "exp_name": f"test_tnn/test_{len(pixels)}_pixel_forward/{idx}/{num}"
        ,"save_smt":True
    }
    use_stack = False
    result = run_dnnct.run(
        model_name, in_dict, con_dict,model_type='tnn',
        save_exp=save_exp, norm=True, solve_order_stack=use_stack,
        max_iter=0, total_timeout=3600, single_timeout=1800, timeout=1800,
        limit_change_range=110,
    )
    
    recorder = result[1]
    original_input = np.squeeze(mnist_dataset.get_origin_mnist_test_data(idx=idx))
    adversarial_input = np.squeeze(recorder.adversarial_input)
    if adversarial_input.size <= 1:
        return 0
    if check_origin_cnn_result(idx,original_input,adversarial_input):
        return 1
    else:
        return 0

def sixty_pixel_test(num,idx,pixels):
    idx = idx
    in_dict, con_dict = mnist_dataset.get_mnist_test_data(idx=idx)

    for i in pixels:
        con_dict[i]=1
    save_exp = {
        "input_name": f"mnist_test_{idx}",
        "exp_name": f"test_tnn/test_{len(pixels)}_pixel_forward/{idx}/{num}"
        ,"save_smt":True
    }
    use_stack = False
    result = run_dnnct.run(
        model_name, in_dict, con_dict,model_type='tnn',
        save_exp=save_exp, norm=True, solve_order_stack=use_stack,
        max_iter=0, total_timeout=1200, single_timeout=600, timeout=1200,
        limit_change_range=110,
    )
    
    recorder = result[1]
    original_input = np.squeeze(mnist_dataset.get_origin_mnist_test_data(idx=idx))
    adversarial_input = np.squeeze(recorder.adversarial_input)
    if adversarial_input.size <= 1:
        return 0
    if check_origin_cnn_result(idx,original_input,adversarial_input):
        return 1
    else:
        return 0
    
   
    # print("\nTotal iterations:", result[0])
    # test_one_pixel_forward()
#limit_change_range會*0.2
def shap_pixel_test(num,idx,rows,cols):
    start_time = time.time()
    idx = idx
    in_dict, con_dict = mnist_dataset.get_mnist_test_data(idx=idx)
    for i in range(num+1):
            con_dict[f"v_{rows[i]}_{cols[i]}_0"]=1
    save_exp = {
        "input_name": f"mnist_test_{idx}",
        "exp_name": f"test_tnn_delta/test_{num}_pixel_forward/{idx}"
        ,"save_smt":True
    }
    # save_exp = {
    #     "input_name": f"mnist_test_{idx}",
    #     "exp_name": f"test_tnn/test_{num}_pixel_forward/{idx}"
    #     ,"save_smt":True
    # }
    use_stack = False
    result = run_dnnct.run(
        model_name, in_dict, con_dict,model_type='tnn',
        save_exp=save_exp, norm=True, solve_order_stack=use_stack,
        max_iter=0, total_timeout=600, single_timeout=600, timeout=600,
        limit_change_range=500,
    )
    
    recorder = result[1]
    total_time = time.time() - start_time
    file_path=f'{save_exp["exp_name"]}'
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    with open(f'{file_path}/total_time', 'w') as file:
            file.write('Total execution time: {} seconds'.format(total_time))
    if recorder.attack_label!=None:
        return 1
    else:
        return 0
    
def shap_pixel_timeout_test(num,idx,rows,cols,time_out=100):
    start_time = time.time()
    idx = idx
    in_dict, con_dict = mnist_dataset.get_mnist_test_data(idx=idx)
    for i in range(num+1):
            con_dict[f"v_{rows[i]}_{cols[i]}_0"]=1
    # save_exp = {
    #     "input_name": f"mnist_test_{idx}",
    #     "exp_name": f"test_tnn_delta_timeout/test_{num}_pixel_forward/{idx}"
    #     ,"save_smt":True
    # }
    save_exp = {
        "input_name": f"mnist_test_{idx}",
        "exp_name": f"test_tnn_timeout/test_{num}_pixel_forward/{idx}"
        ,"save_smt":True
    }
    use_stack = False
    result = run_dnnct.run(
        model_name, in_dict, con_dict,model_type='tnn',
        save_exp=save_exp, norm=True, solve_order_stack=use_stack,
        max_iter=0, total_timeout=time_out, single_timeout=time_out, timeout=time_out,
        limit_change_range=500,
    )
    recorder = result[1]
    time_out = recorder.is_timeout
    total_time = time.time() - start_time
    file_path=f'{save_exp["exp_name"]}'
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    with open(f'{file_path}/timeout', 'w') as file:
            file.write('Time out'.format(time_out))
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    with open(f'{file_path}/total_time', 'w') as file:
            file.write('Total execution time: {} seconds'.format(total_time))
    return recorder