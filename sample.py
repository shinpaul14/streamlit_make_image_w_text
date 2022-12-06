import numpy as np



import sys

import urllib



#-------------------
import time
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import keras_cv
from tensorflow import keras
import matplotlib.pyplot as plt
import streamlit as st
#---------------------


def main():
    st.title("Streamlit Face-GAN Demo")
    """This demo demonstrates  using [Nvidia's Progressive Growing of GANs](https://research.nvidia.com/publication/2017-10_Progressive-Growing-of) and 
    Shaobo Guan's [Transparent Latent-space GAN method](https://blog.insightdatascience.com/generating-custom-photo-realistic-faces-using-ai-d170b1b59255) 
    for tuning the output face's characteristics. For more information, check out the tutorial on [Towards Data Science](https://towardsdatascience.com/building-machine-learning-apps-with-streamlit-667cef3ff509)."""



    # Read in models from the data files.


    st.sidebar.title("Features")
    seed = 27834096
    # If the user doesn't want to select which features to control, these will be used.
    default_control_features = ["Young", "Smiling", "Male"]

    if st.sidebar.checkbox("Show advanced options"):
        # Randomly initialize feature values.
        features = get_random_features(feature_names, seed)

        # Some features are badly calibrated and biased. Removing them
        block_list = ["Attractive", "Big_Lips", "Big_Nose", "Pale_Skin"]
        sanitized_features = [
            feature for feature in features if feature not in block_list
        ]

        # Let the user pick which features to control with sliders.
        control_features = st.sidebar.multiselect(
            "Control which features?",
            sorted(sanitized_features),
            default_control_features,
        )
    else:
        features = get_random_features(feature_names, seed)
        # Don't let the user pick feature values to control.
        control_features = default_control_features

    # Insert user-controlled values from sliders into the feature vector.
    for feature in control_features:
        features[feature] = st.sidebar.slider(feature, 0, 100, 50, 5)

    st.sidebar.title("Note")
    st.sidebar.write(
        """Playing with the sliders, you _will_ find **biases** that exist in this
        model.
        """
    )
    st.sidebar.write(
        """For example, moving the `Smiling` slider can turn a face from masculine to
        feminine or from lighter skin to darker. 
        """
    )
    st.sidebar.write(
        """Apps like these that allow you to visually inspect model inputs help you
        find these biases so you can address them in your model _before_ it's put into
        production.
        """
    )
    st.sidebar.caption(f"Streamlit version `{st.__version__}`")

    # Generate a new image from this feature vector (or retrieve it from the cache).
    with session.as_default():
        image_out = generate_image(
            
        )

    st.image(image_out, use_column_width=True)




def get_random_features(feature_names, seed):
    """
    Return a random dictionary from feature names to feature
    values within the range [40,60] (out of [0,100]).
    """
    np.random.seed(seed)
    features = dict((name, 40 + np.random.randint(0, 21)) for name in feature_names)
    return features


# Hash the TensorFlow session, the pg-GAN model, and the TL-GAN model by id
# to avoid expensive or illegal computations.
@st.experimental_memo(show_spinner=False, ttl=24*60*60)
def generate_image():
    """
    Converts a feature vector into an image.
    """
    model = keras_cv.models.StableDiffusion(img_width=512, img_height=512)


    images = model.text_to_image("photograph of an astronaut riding a horse", batch_size=1)








    return images[0]

if __name__ == "__main__":
    main()