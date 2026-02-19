def generate_llm_explanation(drug, gene, star, risk_label):
    return (
        f"For {drug}, gene {gene} with diplotype {star} "
        f"indicates a risk classification of '{risk_label}' "
        f"based on pharmacogenomic guidelines."
    )
