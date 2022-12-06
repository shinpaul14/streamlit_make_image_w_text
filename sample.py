import streamlit as st


# model = keras_cv.models.StableDiffusion(img_width=512, img_height=512)


# images = model.text_to_image("photograph of an astronaut riding a horse", batch_size=1)

st.title('We Art')


# from PIL import Image
# image = Image.open(images)
	
# st.image(image)

age = st.slider('How old are you?', 0, 130, 25)
st.write("I'm ", age, 'years old')