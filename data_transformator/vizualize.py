import json
from pathlib import Path

import statistics
import PIL.Image
import pandas as pd #dask when pandas will be slow

import plotly.graph_objects as go
from plotly.subplots import make_subplots

# image_list = glob.glob('256_ObjectCategories/*/*.jpg')
# print(len(image_list))


#get sample of the query (images + json), show 10 randon images + description, show statistics, counts etc

def show_img(img):
    plt.figure(figsize=(18,15))
    # unnormalize
    img = img / 2 + 0.5  
    npimg = img.numpy()
    npimg = np.clip(npimg, 0., 1.)
    plt.imshow(np.transpose(npimg, (1, 2, 0)))
    plt.show()

def get_samples():
    pass

def show_histogram():
    pass

def show_samples():
    pass 
