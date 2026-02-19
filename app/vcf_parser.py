def parse_vcf(file_text: str):
    """
    Parses a VCF file string and extracts pharmacogenomic variants
    based on GENE and STAR annotations in the INFO field.
    """

    variants = []

    for line in file_text.splitlines():

        # Skip header lines
        if line.startswith("#"):
            continue

        fields = line.strip().split("\t")

        # Ensure valid VCF row
        if len(fields) < 10:
            continue

        chromosome = fields[0]
        try:
            position = int(fields[1])
        except ValueError:
            continue

        rsid = fields[2]
        info_field = fields[7]
        genotype = fields[9]

        gene = None
        star = None

        # Parse INFO column
        info_parts = info_field.split(";")

        for item in info_parts:
            if item.startswith("GENE="):
                gene = item.split("=")[1]
            elif item.startswith("STAR="):
                star = item.split("=")[1]

        # Only add if gene annotation exists
        if gene:
            variants.append({
                "gene": gene,
                "star": star if star else "Unknown",
                "rsid": rsid,
                "chromosome": chromosome,
                "position": position,
                "genotype": genotype
            })

    return variants
