def parse_vcf(file_text: str):
    variants = []

    for line in file_text.splitlines():

        if line.startswith("#"):
            continue

        fields = line.strip().split("\t")

        if len(fields) < 10:
            continue

        chromosome = fields[0]
        position = int(fields[1])
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
            if item.startswith("STAR="):
                star = item.split("=")[1]

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
