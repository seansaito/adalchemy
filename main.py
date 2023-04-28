"""
Streamlit app
Author: Sean Saito

"""

import tempfile
from io import BytesIO

import setuptools.dist
# Import required libraries
import streamlit as st
from PIL import Image
from streamlit_extras.app_logo import add_logo

from src.generator import generate_images, generate_text
from src.utils import create_pdf

import random


def set_selected_id(key, index):
    st.session_state[key] = index

# Function to display a grid of selectable elements
def display_selectable_grid(elements, element_type, num_columns=3):
    selected_element = None
    if elements:
        num_elements = len(elements)
        num_rows = (num_elements + num_columns - 1) // num_columns

        for row in range(num_rows):
            cols = st.columns(num_columns)
            for col_index in range(num_columns):
                index = row * num_columns + col_index
                if index < num_elements:
                    element = elements[index]
                    if element_type == "image":
                        col_image = Image.open(BytesIO(element))
                        # cols[col_index].button(f"Select Image {index+1}", on_click=set_selected_id, args=("image", index))
                        cols[col_index].image(col_image, width=200)
                    elif element_type == "text":
                        cols[col_index].button(f"Option {index+1}", on_click=set_selected_id, args=("text", index), disabled=True)
                        cols[col_index].write(element)

    # return selected_element

def add_logo_custom():
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"] {
                background-image: url(http://placekitten.com/200/200);
                background-repeat: no-repeat;
                padding-top: 120px;
                background-position: 20px 20px;
            }
            [data-testid="stSidebarNav"]::before {
                content: "My Company Name";
                margin-left: 20px;
                margin-top: 20px;
                font-size: 30px;
                position: relative;
                top: 100px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

# Main Streamlit app
def main():
    st.set_page_config(page_icon='assets/favicon.png',
                       page_title='AdAlchemy')
    # Config
    # Import CSS styles
    # with open('assets/styles.css', encoding='utf8') as f:
    #     st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    st.session_state.clear()

    # Logo
    add_logo('./assets/finx_logo.png')
    # add_logo_custom()

    # Sidebar
    st.sidebar.subheader("AdAlchemy")
    image_style = st.sidebar.radio(
        "Select the style for the AI-generated image:",
        ["Anime, Ghibli", "Photorealistic", "Futuristic, Sci-Fi"]
    )
    num_image_options = st.sidebar.slider("Number of image options to generate:", min_value=1, max_value=10)
    num_text_options = st.sidebar.slider("Number of text options to generate:", min_value=1, max_value=10)
    st.sidebar.info(f'''Logged in: **Sean Saito**''')

    ######

    st.title("Welcome to AdAlchemy")
    st.markdown("Use this app to generate images and texts for marketing content.")

    # Input for the topic of the article
    topic = st.text_input("Enter the topic of the article:", value="New life campaign article")

    # Input for the tags/components of the AI-generated image
    st.subheader("Describe the image (tags, components, style, etc.)")

    tags = []
    list_defaults = [
        "Spring, sunny",
        "Good weather, blue skies",
        "Happy, lively atmosphere",
        'Tokyo shopping district such as Harajuku',
        "People walking around",
    ]
    for i in range(5):
        tag = st.text_input(f"Tag {i + 1}:", key=f"tag{i + 1}", value=list_defaults[i])
        if tag:
            tags.append(tag)

    # Generate button
    generate_button = st.button("Generate")

    # Generate images and display them in a carousel
    images = []
    texts = []

    if generate_button:
        if topic and tags:
            images = generate_images(topic, tags, image_style, num_image_options)

            # Generate text and display it in a carousel
            texts = generate_text(topic, num_text_options)

            st.subheader("Generated Images:")
            display_selectable_grid(images, "image")

            # if texts:
            st.subheader("Generated Texts:")
            display_selectable_grid(texts, "text", num_columns=1)

            # Download the finalized PDF
            st.subheader("Download:")

    if images and texts:
        st.text("WIP: still figuring out how to do dynamic selection in Streamlit, \n"
                "so this will produce a PDF based on a random pair of image and text 😅")
        selected_image = random.choice(images)
        selected_text = random.choice(texts)

        pdf = create_pdf(selected_image, selected_text, topic)

        # Save the PDF to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
            tmp_pdf.write(pdf)
            tmp_pdf.flush()

        with open(tmp_pdf.name, "rb") as file:
            pdf_bytes = file.read()
            st.download_button(
                label="Download PDF",
                data=pdf_bytes,
                file_name=f"{topic}.pdf",
                mime="application/pdf",
            )


if __name__ == "__main__":
    main()