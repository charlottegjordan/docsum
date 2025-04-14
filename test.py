import argparse
import os
import base64
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from groq import Groq
import groq
from PyPDF2 import PdfReader
from PyPDF2.errors import PdfReadError

# ---- Parse args ----
parser = argparse.ArgumentParser(prog='docsum', description='summarize the input')
parser.add_argument('filename')
args = parser.parse_args()

# ---- Load .env and set up client ----
load_dotenv()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# ---- Utility: LLM ----
def llm(text):
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": text}],
        model="llama3-8b-8192",
    )
    return chat_completion.choices[0].message.content

# ---- Text chunking ----
def split_text(text, max_chunk_size=1000):
    return [text[i:i+max_chunk_size] for i in range(0, len(text), max_chunk_size)]

# ---- Summarization ----
def summarize_text(text):
    prompt = f"Summarize the following text in 1-3 sentences.\n\n{text}"
    try:
        return llm(prompt).split('\n')[-1]
    except groq.APIStatusError:
        chunks = split_text(text, 10000)
        summaries = [summarize_text(chunk) for chunk in chunks]
        return summarize_text(' '.join(summaries))

# ---- Encode image to base64 ----
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# ---- LLM for local images ----
def llm_image_local(image_path):
    base64_image = encode_image(image_path)
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "user", "content": [
                {"type": "text", "text": "What's in this image?"},
                {"type": "image_url", "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"}
                },
            ]}
        ],
        model="llama-3.2-11b-vision-preview",
    )
    return chat_completion.choices[0].message.content

# ---- LLM for image URLs ----
def llm_image_url(image_path):
    completion = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {"role": "user", "content": [
                {"type": "text", "text": "What's in this image?"},
                {"type": "image_url", "image_url": {"url": image_path}}
            ]}
        ],
        temperature=1,
        max_completion_tokens=1024,
    )
    return completion.choices[0].message.content

# ---- Helpers ----
def is_image_url(path):
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
    return any(path.lower().endswith(ext) for ext in image_extensions)

def is_url(path):
    return path.startswith("http://") or path.startswith("https://")

def fetch_text_from_url(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, features="lxml")
    return soup.get_text()

# ---- Main logic ----
if is_url(args.filename):
    if is_image_url(args.filename):
        print(llm_image_url(args.filename))
    else:
        text = fetch_text_from_url(args.filename)
        print(summarize_text(text))
else:
    try:
        with open(args.filename, 'r') as fin:
            html = fin.read()
            soup = BeautifulSoup(html, features="lxml")
            text = soup.get_text()
            print(summarize_text(text))
    except UnicodeDecodeError:
        try:
            with open(args.filename, 'rb') as fin:
                reader = PdfReader(fin)
                text = ''
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                print(summarize_text(text))
        except PdfReadError:
            try:
                print(llm_image_local(args.filename))
            except:
                print('something is wrong')
