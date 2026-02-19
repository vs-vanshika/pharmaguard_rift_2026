def parse_vcf(file_text: str):
    """
    Custom lightweight VCF parser (no pysam).
    Extracts:
    - chromosome
    - position
    - rsid
    - gene
    - star allele
    - genotype
    """

    variants = []

    lines = file_text.splitlines()

    for line in lines:
        if line.startswith("#"):
            continue  # Skip headers

        parts = line.strip().split("\t")

        if len(parts) < 10:
            continue

        chrom = parts[0]
        pos = parts[1]
        rsid = parts[2]
        info = parts[7]
        genotype = parts[9]

        # Parse INFO field
        info_dict = {}
        for item in info.split(";"):
            if "=" in item:
                key, value = item.split("=")
                info_dict[key] = value

        variants.append({
            "chromosome": chrom,
            "position": int(pos),
            "rsid": rsid,
            "gene": info_dict.get("GENE", "Unknown"),
            "star": info_dict.get("STAR", "*1"),
            "genotype": genotype
        })

    return variants
