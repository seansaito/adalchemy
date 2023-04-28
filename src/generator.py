import os
import warnings
from typing import Optional

import streamlit as st
import openai
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
from stability_sdk import client

# Our Host URL should not be prepended with "https" nor should it have a trailing slash.
os.environ['STABILITY_HOST'] = 'grpc.stability.ai:443'
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to generate images using an AI image generation API (e.g. DALL-E)
def generate_images(topic, tags, style, num_images) -> Optional[list[bytes]]:
    if topic is None:
        return None
    # Call the API with the topic, tags, and style as parameters
    # Here we should use the appropriate function to call the desired API

    # Set up our connection to the API.
    stability_api = client.StabilityInference(
        key=os.environ['STABILITY_KEY'],  # API Key reference.
        verbose=True,  # Print debug messages.
        engine="stable-diffusion-xl-beta-v2-2-2",  # Set the engine to use for generation.
    )

    # Generate the prompt
    prompt = """
    Create a banner image for a marketing article with the topic {topic}
    with the following components {tags}
    with the following style {style}
    """.format(
        topic=topic,
        tags=", ".join(tags),
        style=style
    )

    # Set up our initial generation parameters.
    answers = stability_api.generate(
        prompt=prompt,
        steps=30, # Amount of inference steps performed on image generation. Defaults to 30.
        cfg_scale=8.0, # Influences how strongly your generation is guided to match your prompt.
                       # Setting this value higher increases the strength in which it tries to match your prompt.
                       # Defaults to 7.0 if not specified.
        width=512, # Generation width, defaults to 512 if not included.
        height=512, # Generation height, defaults to 512 if not included.
        samples=num_images, # Number of images to generate, defaults to 1 if not included.
        sampler=generation.SAMPLER_K_DPMPP_2M
    )

    # Set up our warning to print to the console if the adult content classifier is tripped.
    # If adult content classifier is not tripped, save generated images.
    list_results = []
    for resp in answers:
        for artifact in resp.artifacts:
            if artifact.finish_reason == generation.FILTER:
                warnings.warn(
                    "Your request activated the API's safety filters and could not be processed."
                    "Please modify the prompt and try again.")
            if artifact.type == generation.ARTIFACT_IMAGE:
                list_results.append(artifact.binary)

    return list_results


# Function to generate text using an AI text generation API (e.g. GPT-3)
def generate_text(topic, num_texts) -> Optional[list[str]]:
    if topic is None:
        return None

    # Call the API with the topic as a parameter
    # Here we should use the appropriate function to call the desired API
    prompt = """
    You are an expert marketing editor/content creator/creative director.
    
    Please write an eye-catching marketing campaign article on the following topic: {topic}
    
    """.format(topic=topic)

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user",
             "content": prompt}
        ],
        n=num_texts,
    )

    list_results = [choice.message['content'] for choice in completion.choices]

    return list_results
