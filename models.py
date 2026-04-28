from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

def compute_similarity(resume_text, job_desc):
    embeddings = model.encode([resume_text, job_desc])
    score = util.cos_sim(embeddings[0], embeddings[1]).item()
    return round(score * 100, 2)

def predict_score(similarity, skill_match):
    final = (0.7 * similarity) + (0.3 * skill_match)

    if final > 80:
        return final, "High Chance ✅"
    elif final > 60:
        return final, "Medium Chance ⚠️"
    else:
        return final, "Low Chance ❌"