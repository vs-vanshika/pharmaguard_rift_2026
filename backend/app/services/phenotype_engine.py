def determine_phenotype(gene: str, diplotype: str):
    """
    Map STAR allele diplotypes to phenotype (simplified CPIC logic)
    """
    if diplotype in ["*1/*1"]:
        return "NM"  # Normal metabolizer
    elif diplotype in ["*1/*2", "*1/*3"]:
        return "IM"  # Intermediate metabolizer
    elif diplotype in ["*2/*2", "*3/*3", "*4/*4"]:
        return "PM"  # Poor metabolizer
    elif diplotype in ["*1/*17"]:
        return "URM"  # Ultra-rapid metabolizer
    else:
        return "Unknown"
