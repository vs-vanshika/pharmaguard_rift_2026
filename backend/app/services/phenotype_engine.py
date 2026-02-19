def determine_phenotype(gene: str, diplotype: str):
    """
    Determine metabolizer phenotype based on gene and diplotype.
    Simplified CPIC-aligned demo logic.
    """

    if diplotype in ["*1/*1"]:
        return "NM"

    if diplotype in ["*1/*2", "*1/*3"]:
        return "IM"

    if diplotype in ["*2/*2", "*3/*3", "*4/*4"]:
        return "PM"

    if diplotype in ["*1/*17"]:
        return "URM"

    return "Unknown"
