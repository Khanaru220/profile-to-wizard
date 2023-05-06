from dotenv import load_dotenv
import os
# from gradio.mix import Series, Parallel
# from transformers import pipeline
import gradio as gr
import json
import requests
import io
from PIL import Image

# Store var with .env: https://www.realpythonproject.com/3-ways-to-store-and-read-credentials-locally-in-python/
load_dotenv()
token = os.environ.get('API_TOKEN')

API_URL_1 = "https://api-inference.huggingface.co/models/gpt2"
API_URL_2 = "https://api-inference.huggingface.co/models/prompthero/openjourney"
headers = {"Authorization": f"Bearer {token}"}


# Covert JSON to Object: https://stackoverflow.com/a/15882054/14733188
def query(url, payload):
    data = json.dumps(payload)
    response = requests.request("POST", url, headers=headers, data=data)
    return json.loads(response.content.decode('utf-8'))


def queryImg(url, payload):
    data = json.dumps(payload)
    response = requests.request("POST", url, headers=headers, data=data)
    return response.content


def greet(name, technology, magicPreference, gender, os, yearsPratice):
    genreForPrompt = "<superhero>"
    initDisplayText = 'Welcome {name}.\nHaving {yearsPratice} years of practicing is pretty good.\nShow me some tricks in {technology}.\n\n...'.format(
        name=name.title(), yearsPratice=yearsPratice, os=' ,'.join(os), technology=technology.title())

    promptForStory = "{} I'm a wizard ".format(genreForPrompt)

    promptForImg = 'mdjrny-v4 style portrait of {name}, a {gender} ((developer)), {ages} years old , wearing wizard cloths, hand casting spell,  (({technology})) logo, {lightTheme}, elegant, highly detailed, digital painting, artstation, concept art, smooth, cyperpunk, sharp focus, illustration, art by artgerm and greg rutkowski and alphonse mucha, 8k'.format(
        name=name, gender="male" if gender == "Male" else "female", ages=yearsPratice*4+8, os=' ,'.join(os), technology=technology, lightTheme='bright' if magicPreference == 'White magic' else 'darkest serious')
    print(promptForImg)

    AICreatedStory = query(API_URL_1, {"inputs": promptForStory, "options": {
                           "wait_for_model": True, "use_cache": False}})[0]['generated_text']
    print(queryImg(API_URL_2, {
          "inputs": promptForImg, "options": {"wait_for_model": True}}))
    return initDisplayText + AICreatedStory[len(genreForPrompt):], Image.open(io.BytesIO(queryImg(API_URL_2, {"inputs": promptForImg, "options": {"wait_for_model": True}})))


demo = gr.Interface(fn=greet, inputs=[gr.Textbox(label="Wizard's name:", placeholder="e.g, John Doe"), gr.Textbox(
    label="Your magic:", placeholder='e.g, C#, Python'), gr.Radio(label="Preference:", choices=["Dark magic", "White magic"]), gr.Radio(label='Gender:', choices=["Male", 'Female', 'Guess']), gr.CheckboxGroup(label='Show me your wands:', choices=['MacOS', 'Linux', 'Windows']),  gr.Slider(label='Years of magic praticing:', minimum=0, maximum=15, step=0.5, randomize=True)], outputs=[gr.Textbox(label="Our first meeting"), gr.Image(label="Portrait")])

if __name__ == "__main__":
    # Series(interface).launch()
    demo.launch()
