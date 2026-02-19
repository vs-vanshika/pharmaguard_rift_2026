import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_explanation(drug: str, gene: str, phenotype: str):
    prompt = f"""
    Provide a clinical pharmacogenomic explanation for prescribing {drug}
    in a patient with {gene} {phenotype} phenotype.
    Include:
    - Biological metabolism mechanism
    - Impact of genetic variants
    - Clinical dosing reasoning
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a pharmacogenomics clinical expert."},
            {"role": "user", "content": prompt}
        ]
    )

    text = response.choices[0].message.content
    return {
        "summary": text,
        "mechanism": "Detailed in summary",
        "variant_interpretation": "Detailed in summary"
    }
