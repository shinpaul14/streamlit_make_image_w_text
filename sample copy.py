
import time
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import keras_cv
from tensorflow import keras
import matplotlib.pyplot as plt
import streamlit as st

# model = keras_cv.models.StableDiffusion(img_width=512, img_height=512)


# images = model.text_to_image("photograph of an astronaut riding a horse", batch_size=1)
# print(type(images))





# from PIL import Image
# image = Image.fromarray(images)
# # image = Image.open('sunrise.jpg')

# st.image(image, caption='photograph of an astronaut riding a horse')