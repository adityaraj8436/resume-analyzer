import streamlit as st
import pandas as pd
import requests
from streamlit_lottie import st_lottie

from utils import extract_text_from_pdf, clean_text, extract_skills
from model import compute_similarity, predict_score
from skills import SKILLS

st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

# 🔐 LOGIN
USERNAME = "admin"
PASSWORD = "1234"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    st.title("🔐 Login")
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")
    if st.button("Login"):
        if u == USERNAME and p == PASSWORD:
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Invalid credentials")

if not st.session_state.logged_in:
    login()
    st.stop()

if st.button("🚪 Logout"):
    st.session_state.logged_in = False
    st.rerun()

# 🎥 Animation
def load_lottie(url):
    return requests.get(url).json()

anim = load_lottie("https://assets5.lottiefiles.com/packages/lf20_kyu7xb1v.json")

# 🎨 CSS
st.markdown("""
<style>
.block-container {animation: fadeIn 0.8s;}
@keyframes fadeIn {0%{opacity:0;}100%{opacity:1;}}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center;'>🚀 Resume Analyzer</h1>", unsafe_allow_html=True)
st_lottie(anim, height=200)

col1, col2 = st.columns(2)

with col1:
    job_desc = st.text_area("Job Description")

with col2:
    files = st.file_uploader("Upload Resumes", type=["pdf"], accept_multiple_files=True)

results = []

if files and job_desc:
    clean_job = clean_text(job_desc)
    job_skills = extract_skills(clean_job, SKILLS)

    for f in files:
        text = extract_text_from_pdf(f)
        clean_resume = clean_text(text)

        sim = compute_similarity(clean_resume, clean_job)
        res_skills = extract_skills(clean_resume, SKILLS)

        matched = list(set(res_skills) & set(job_skills))
        skill_score = (len(matched)/len(job_skills))*100 if job_skills else 0

        final, pred = predict_score(sim, skill_score)

        results.append({
            "Name": f.name,
            "Score": round(final, 2),
            "Prediction": pred
        })

    df = pd.DataFrame(results).sort_values(by="Score", ascending=False)

    st.dataframe(df)
    st.bar_chart(df.set_index("Name")["Score"])