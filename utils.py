import pdfplumber
import re

def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            if page.extract_text():
                text += page.extract_text() + " "
    return text

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z ]', ' ', text)
    return text

def extract_skills(text, skills_list):
    text = text.lower()
    found = set()
    for skill in skills_list:
        if skill in text:
            found.add(skill)
    return list(found)