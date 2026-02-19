def parse_vcf(file):
    variants = []
    supported_gene_detected = False

    for line in file:
        if line.startswith("#"):
            continue

        columns = line.strip().split("\t")
        chrom, pos, _, ref, alt, _, _, info = columns[:8]

        info_dict = {}
        for field in info.split(";"):
            if "=" in field:
                key, value = field.split("=")
                info_dict[key] = value

        gene = info_dict.get("GENE")
        rsid = info_dict.get("RS", "unknown")

        if gene in ["CYP2D6", "CYP2C19", "CYP2C9", "SLCO1B1", "TPMT", "DPYD"]:
            supported_gene_detected = True

            variants.append({
                "rsid": rsid,
                "chromosome": chrom,
                "position": int(pos),
                "ref": ref,
                "alt": alt,
                "gene": gene
            })

    return variants, supported_gene_detected
