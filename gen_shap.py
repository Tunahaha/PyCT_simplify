import keras
import shap
import numpy as np
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from utils.dataset import MnistDataset
import test_dnnct_cnn 
import test_dnnct_tnn
import time
import pandas as pd
import concurrent.futures
import os
from multiprocessing import Pool




mnist_dataset = MnistDataset()
model = keras.models.load_model('model/mnist_sep_act_m6_9628.h5')
def get_dataset(idx):
    origin_input=mnist_dataset.get_origin_mnist_test_data(idx)
    origin_input=np.expand_dims(origin_input,axis=0)
    return origin_input
    
def get_background():
    x_train=mnist_dataset.get_x_test()
    background = x_train[0:100]
    return background

def get_shap(idx, model):  
    background = get_background()
    explainer = shap.DeepExplainer(model, background)
    print("start")
    simple_data=get_dataset(idx)
    x_test_sample = simple_data[0:1]
    shap_values = explainer.shap_values(x_test_sample)
    predicted_class = mnist_dataset.get_y_test(idx)
    shap_values_class = shap_values[predicted_class]
    abs_shap_values = np.abs(shap_values_class)
    flat_shap_values = abs_shap_values.flatten()
    top_pixels = np.argpartition(flat_shap_values, -16)[-16:]
    top_pixels_sorted_by_value = sorted(top_pixels, key=lambda x: flat_shap_values[x], reverse=True)
    top_pixels_positions = np.unravel_index(top_pixels_sorted_by_value, abs_shap_values.shape)
    df = pd.DataFrame({
            'row': [top_pixels_positions[1].tolist()],
            'col': [top_pixels_positions[2].tolist()]
        })
    return df

shap_values_df = pd.DataFrame()
for i in range(5000):
    df = get_shap(i, model)
    shap_values_df = pd.concat([shap_values_df, df], ignore_index=True)
shap_values_df.to_csv('shap/shap_values.csv', index=False)
# df=pd.read_csv('shap/shap_values.csv')
# print(df.iloc[0,0])