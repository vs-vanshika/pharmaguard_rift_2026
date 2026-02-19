DRUG_GENE_MAP = {
    "CODEINE": "CYP2D6",
    "CLOPIDOGREL": "CYP2C19",
    "WARFARIN": "CYP2C9",
    "SIMVASTATIN": "SLCO1B1",
    "AZATHIOPRINE": "TPMT",
    "FLUOROURACIL": "DPYD"
}


def assess_risk(drug: str, phenotype: str):
    if phenotype == "PM":
        return "Toxic", 0.9, "high"
    elif phenotype == "IM":
        return "Adjust Dosage", 0.8, "moderate"
    elif phenotype == "NM":
        return "Safe", 0.95, "none"
    elif phenotype == "URM":
        return "Ineffective", 0.85, "moderate"
    else:
        return "Unknown", 0.5, "low"
