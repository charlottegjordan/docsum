# PARSER STUFF/IMPORTS
import argparse
parser = argparse.ArgumentParser(
    prog='docsum',
    description='summarize the input',
    )

parser.add_argument('filename')
args = parser.parse_args()


from dotenv import load_dotenv
load_dotenv()

import os
from groq import Groq
import groq
import base64
import mimetypes


#ADDING KEY
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)
def llm(text):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": text,
            }
        ],
        model="llama3-8b-8192",
    )
    return chat_completion.choices[0].message.content






#SPLITTING CHUNKS / MAIN SUMMARIZER FUNCTION FOR TEXT
def split_text(text, max_chunk_size=1000):
    '''
    Takes a string as input and returns a list of strings that are all smaller than max chunk size)
    >>> split_text('abcdefg', max_chunk_size=2)
    ['ab', 'cd', 'ef', 'g']
    '''
    accumulator = []
    while len(text) > 0:
        accumulator.append(text[:max_chunk_size])
        text = text[max_chunk_size:]
    return accumulator

def summarize_text(text):
    prompt = f"""
    Summarize the following text in 1-3 sentences.

    {text}
    """
    try:
        output = llm(prompt)
        return output.split('\n')[-1]
    except groq.APIStatusError:
        chunks = split_text(text, 10000)
        print("len(chunks)=", len(chunks))
        accumulator = []
        for i, chunk in enumerate(chunks):
            print('i=', i)
            summary = summarize_text(chunk)
            accumulator.append(summary)
        summarized_text = ' '.join(accumulator)
        summarized_text = summarize_text(summarized_text)
        return summarized_text


# FILE TYPE CHECKER
def get_mime_type(image_path):
    mime_type, _ = mimetypes.guess_type(image_path)
    return mime_type or "image/png"


# IMAGE RELATED FUNCTIONS
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

def llm_image(image_path = None, url = None):
    if image_path != None and url == None:
        base64_image = encode_image(image_path)
        mime_type = get_mime_type(image_path)

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "What's in this image?"},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{mime_type};base64,{base64_image}",
                            },
                        },
                    ],
                }
            ],
            model="llama-3.2-11b-vision-preview",
        )

        return chat_completion.choices[0].message.content


    elif url != None and image_path == None:
        completion = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "What's in this image?"
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": url
                            }
                        }
                    ]
                }
            ],
            temperature=1,
            max_completion_tokens=1024,
            top_p=1,
            stream=False,
            stop=None,
        )

        return(completion.choices[0].message)
        







import requests
from bs4 import BeautifulSoup
from PyPDF2 import PdfReader
from PyPDF2.errors import PdfReadError

try:
    # FOR TXT FILES
    with open(args.filename, 'r') as fin:
        html = fin.read()
        soup = BeautifulSoup(html, features="lxml")
        text = soup.text
        print(summarize_text(text))
except UnicodeDecodeError:
    # FOR PDF FILES
    try:
        with open(args.filename, 'rb') as fin:
            reader = PdfReader(fin)
            text = ''
            for page in reader.pages:
                text += page.extract_text() + "\n"
            print(summarize_text(text))


    except PdfReadError:
        # FOR LOCAL IMAGES
            print(summarize_text(llm_image(args.filename, None)))


except FileNotFoundError:
    # FOR HTML FILES/LINKS  
    try:
        print(summarize_text(llm_image(None, args.filename).content))
    except groq.BadRequestError:
        r = requests.get(args.filename)
        html = r.text
        soup = BeautifulSoup(html, features='lxml')
        text = soup.text
        print(summarize_text(text))

