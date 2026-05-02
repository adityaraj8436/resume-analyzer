import streamlit as st
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# 🚀 Load model only once (VERY IMPORTANT for deployment)
@st.cache_resource
def load_model():
    return SentenceTransformer('all-MiniLM-L6-v2', device='cpu')

model = load_model()


# 🔍 Compute semantic similarity
def compute_similarity(resume_text, job_text):
    if not resume_text or not job_text:
        return 0.0

    embeddings = model.encode([resume_text, job_text])

    similarity = cosine_similarity(
        [embeddings[0]],
        [embeddings[1]]
    )[0][0]

    return float(similarity)


# 🎯 Final scoring logic
def predict_score(similarity, skill_score):
    """
    similarity → semantic match (0–1)
    skill_score → keyword match (0–100)
    """

    # Normalize similarity to percentage
    sim_score = similarity * 100

    # Weighted score (tunable)
    final_score = (0.7 * sim_score) + (0.3 * skill_score)

    # 🎯 Decision thresholds
    if final_score >= 75:
        label = "🟢 Strong Match"
    elif final_score >= 55:
        label = "🟡 Moderate Match"
    else:
        label = "🔴 Weak Match"

    return round(final_score, 2), label