from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def translate_hi_en(text):
    if not text.strip():
        return "No text provided."

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",  # ✅ correct model
        messages=[
            {"role": "system", "content": "You are a legal officer. Translate Hindi FIR/legal text into English internally and output only a concise summary of the incident in English."},
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message.content.strip()
