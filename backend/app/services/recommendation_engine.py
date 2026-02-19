def generate_recommendation(drug, phenotype):
    if phenotype == "PM":
        return (
            "High risk of toxicity detected.",
            "CPIC Level A Guideline",
            "Avoid drug or significantly reduce dosage."
        )
    elif phenotype == "IM":
        return (
            "Reduced metabolism expected.",
            "CPIC Level A Guideline",
            "Consider dose adjustment."
        )
    elif phenotype == "NM":
        return (
            "Normal metabolism expected.",
            "CPIC Level A Guideline",
            "Standard dosing recommended."
        )
    else:
        return (
            "Insufficient data.",
            "CPIC Guideline",
            "Monitor closely."
        )
