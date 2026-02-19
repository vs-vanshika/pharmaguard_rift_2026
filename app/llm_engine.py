def generate_llm_explanation(drug, gene, star, risk_label):

    return (
        f"For {drug}, the primary gene analyzed is {gene}. "
        f"The detected diplotype is {star}. "
        f"This results in a risk classification of '{risk_label}' "
        f"based on established pharmacogenomic guidelines."
    )
