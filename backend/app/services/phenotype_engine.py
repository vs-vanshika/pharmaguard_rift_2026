def determine_phenotype(gene: str, diplotype: str):
    """
    Determine metabolizer phenotype based on gene and diplotype.
    Simplified CPIC-aligned demo logic.
    """
    if gene == "CYP2D6":
        if diplotype == "*4/*4": return "PM"
        if "*4" in diplotype: return "IM"
        return "NM"

    if gene == "CYP2C19":
        if diplotype == "*2/*2": return "PM"
        if "*2" in diplotype: return "IM"
        return "NM"

    return "Unknown"
