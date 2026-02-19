import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    print("⚠ GROQ_API_KEY not found")

client = Groq(api_key=api_key)


def generate_llm_explanation(drug: str, gene: str, star: str, risk_label: str):

    print("📡 Calling Groq API...")

    try:
        prompt = f"""
You are a clinical pharmacogenomics expert.

Drug: {drug}
Gene: {gene}
Diplotype: {star}
Predicted Risk: {risk_label}

Explain:
- Biological mechanism
- How the variant affects metabolism
- Why this leads to the predicted risk
- Keep under 150 words.
"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # ✅ Updated model
            messages=[
                {"role": "system", "content": "You are a pharmacogenomics expert."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4,
            max_tokens=300
        )

        explanation_text = response.choices[0].message.content.strip()

        print("✅ Groq response received successfully")

        return explanation_text

    except Exception as e:
        print("❌ Groq API ERROR:", str(e))
        return f"LLM explanation unavailable due to API error. Risk classified as {risk_label}."
