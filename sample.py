import numpy as np

from PIL import Image
import copy
#-------------------
import time
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import keras_cv

import streamlit as st

#---------------------


def main():
    st.title("We-Art")
    """We Art is a web app that allows you to generate images from text. It is based on the paper [Stable Diffusion Models for Text to Image Synthesis](https://arxiv.org/abs/2006.11239)."""
    #------
    with st.expander("ℹ️ How to Construct Perfect Prompt for Image Generation instructions", expanded=False):
        st.markdown(
            """
            ### How to write the perfect prompt for image generation
            To try this web, you first need to specify your Image type and size:
            [Best 100+ Stable Diffusion Prompts: The Most Beautiful AI Text-to-Image Prompts](https://archive.md/KDMTA)

            """
        )
        st.markdown("")
        st.code(
            """
            [Example 1]
            # Enter your Prompt here:
            portrait photo of a african old warrior chief, tribal panther make up, gold on white, side profile, looking away, serious eyes, 50mm portrait photography, hard rim lighting photography beta ar 2:3 beta
            """
        )
        st.markdown("")
        st.code(
            """
            [Example 2]
            # Enter your Prompt here:
            portrait photo headshot by mucha, sharp focus, elegant, render, octane, detailed, award winning photography, masterpiece, rim lit
            """
        )
        st.markdown("")
        st.code(
            """
            [Example 3]
            # Enter your Prompt here:
            very complex hyper-maximalist overdetailed cinematic tribal fantasy closeup macro portrait of a heavenly beautiful young royal dragon queen with long platinum blonde windblown hair and dragon scale wings, Magic the gathering, pale wet skin and dark eyes and red lipstick ,flirting smiling passion seductive, vibrant high contrast, by andrei riabovitchev, tomasz alen kopera,moleksandra shchaslyva, peter mohrbacher, Omnious intricate, octane, moebius, arney freytag, Fashion photo shoot, glamorous pose, trending on ArtStation, dramatic lighting, ice, fire and smoke, orthodox symbolism Diesel punk, mist, ambient occlusion, volumetric lighting, Lord of the rings, BioShock, glamorous, emotional, tattoos,shot in the photo studio, professional studio lighting, backlit, rim lighting, Deviant-art, hyper detailed illustration, 8k
            """
        )
        st.markdown(
            """
            Copy above prompt for great quality text to image `CTRL+S or CMD+S`
            """
        )
        st.markdown("")

    #------

    st.sidebar.title("Image Transform")

    # If the user doesn't want to select which features to control, these will be used.
    control_features = ["Height", "Width",]

    features = {}

    # Insert user-controlled values from sliders into the feature vector.
    for feature in control_features:
        features[feature] = st.sidebar.slider(feature, 0, 1024, 512, 1)
    result_by_person = st.sidebar.slider('Rate the satisfaction level of the art work you have received!',0, 100, 50, 1)
    if result_by_person > 90:
        st.sidebar.write('I know this is great!!!')
    elif result_by_person < 90 and result_by_person >= 50:
        st.sidebar.write('Thanks we will harder for improvement')
    else:
        st.sidebar.write('Well I guess back to work than .. thanks....')


    st.sidebar.title("Note")
    st.sidebar.write(
        """Playing with the sliders, you _will_ find **size of an Image** that changes.
        """
    )
    st.sidebar.write(
        """You can choose to write you own prompt and explore you creativity.

        """
    )
    st.sidebar.write(
        """Apps like these that allow you to visually inspect model output and help you
        find these important aspect of generative models key wors so you can address them in your image generation task, before it's put into
        production or real life test.
        """
    )
    st.sidebar.caption(f"Streamlit version `{st.__version__}`")

#--------------------------------------
    choose_form = st.radio(
    "Do you need assistant in making your image?",
    ('No', 'Yes'))
#--------------------------------------
    if choose_form =='No':

        form = st.form(key="Form1")

        with form:
            cols1 = st.columns((1, 1))
            author = cols1[0].text_input("Name of Image Creator:")
            prompt = st.text_area("Prompt text to image:")
            cols2 = st.columns(2)
            date = cols2[0].date_input("Image created date:")
            submitted = st.form_submit_button(label="Generate Image")
            prompt = prompt+'with signture of name {}'.format(author)

        if submitted:
            st.write("The prompt is")
            st.write(prompt)
            image_out = generate_image(str(prompt), features)
    
            st.image(image_out)
    else:

        form_main = st.form(key="template_form")

        with form_main:
            col = st.columns((1, 1))
            author = col[0].text_input("Name of Image Creator:")
            type_of_work = st.selectbox(
            "What type of art work do you want??",
            ('Random','I will write it','portrait photo', 'Photo','photography','concept art',
        'Painting','clear portrait','digital concept art','award winning photography','epic cinematic concept art CG',
        'cinematic shot','Fantasy art','hyper realistic','typography','3d typography','poster','diagram','anime','digital art'))

            Quality = st.selectbox("What kind of quality work do you want??",
            ('Random','I will write it','detailed illustration','HD','4k','16k','3d render','ultrarealistic','professional studio','highly detailed','very complex hyper-maximalist overdetailed','photo realistic',
            'CG render','unreal engine, hyper detailed, photo','high quality','hyperdetailed'))

            Theme = st.selectbox('DO you want to implment Theme',
            ('Random','I will write it','borderlands 3','cyberpunk','MOBA','The Legend of Zelda','Breath of The Wild','Nausicaa Ghibli','studio ghibli','disney animation','pixar'))

            artist_style = st.selectbox('Want to implement the work of popular artist?',
            ('Nope','I will write it','stefan kostic','Yoji Shinkawa','Jackson Pollock','Gerald parel',' Luc Schuiten','Henry Ossawa','Andy Warhol','Carr Clifton & Galen Rowell'
            ,'Dustin Lefevre & tdraw'))
            camera_type = st.selectbox('Type of camera view you can use',
            ('None','3 5 mm camera','85mm lens'))
            special_effect = st.selectbox('Do you want to implement special effect',
            ('None','hard rim lighting','cinematic lighting','sharp focus','dramatic lighting','professional studio lighting','rim lighting','volumetric lighting','dramatic lighting',
            'natural light','lights','dynamic dramatic cinematic lighting','ethereal lights','shafts of lighting','glowing lights','volume twilight','colorful highlights','soft lighting',
            'natural lighting'))
            if type_of_work =='Random':
                type_of_work = ''
            elif type_of_work == 'I will write it':
                type_of_work = st.text_input('Type ...')
            else:
                type_of_work = type_of_work

            if Quality =='Random':
                Quality = ''
            elif Quality == 'I will write it':
                Quality = st.text_input('Type ...')
            else:
                Quality = Quality

            if Theme =='Random':
                Theme = ''
            elif Theme == 'I will write it':
                Theme = st.text_input('Type ...')
            else:
                Theme = Theme

            if artist_style =='Nope':
                artist_style = ''
            elif artist_style == 'I will write it':
                artist_style = st.text_input('Type ...')
            else:
                artist_style = artist_style
            
            if camera_type =='None':
                camera_type = ''
            else:
                camera_type = camera_type

            if special_effect =='None':
                special_effect = ''
            else:
                special_effect = special_effect

            objects = st.text_area("Object you want to make an image:")
            person = st.text_area("Person or character you want to make an image:")
            locations = st.text_area("Location of the image:")
            prompt = '{} {} in {} with {}, {} by {}, {},{}'.format(type_of_work, person,locations,  objects,Theme, artist_style, camera_type, special_effect )
            cols3 = st.columns(2)
            date = cols3[0].date_input("Image created date:")
            submitted = st.form_submit_button(label="Generate Image")

        if submitted:

            st.write("The prompt is")
            st.write(prompt)
            image_out = generate_image(prompt, features)
    
            st.image(image_out)

@st.experimental_memo(show_spinner=False, ttl=24*60*60)
def generate_image(prompt,features):
    """
    Converts a feature vector into an image.
    """
    model = keras_cv.models.StableDiffusion(img_width=512, img_height=512)

#"photograph of an astronaut riding a horse"
    images = model.text_to_image(prompt, batch_size=1)
    img = copy.deepcopy(images[0])
    imgs = Image.fromarray(img)
    imgs = imgs.resize((features['Width'],features['Height']),3)

    return imgs


if __name__ == "__main__":
    main()