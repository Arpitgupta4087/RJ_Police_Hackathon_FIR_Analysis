import os
import pandas as pd
from sentence_transformers import SentenceTransformer, util

os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"


dataset = pd.read_csv("FIR-DATA.csv")
dataset["Offense"] = dataset["Offense"].fillna("").str.strip()
dataset["Description"] = dataset["Description"].fillna("").str.strip()


model = SentenceTransformer("paraphrase-MiniLM-L6-v2")

offense_embeddings = model.encode(dataset["Offense"].tolist(), convert_to_tensor=True)



def predict_ipc_sections(complaint: str, top_k: int = 3):
    """
    Predict most relevant IPC sections for a FIR complaint.
    Returns list of dicts with Offense + Description only.
    """

    complaint_embedding = model.encode(complaint, convert_to_tensor=True)

    similarities = util.cos_sim(complaint_embedding, offense_embeddings)[0]


    top_indices = similarities.argsort(descending=True)[:top_k]


    results = dataset.iloc[top_indices][["Offense", "Description"]].to_dict(orient="records")
    return results


