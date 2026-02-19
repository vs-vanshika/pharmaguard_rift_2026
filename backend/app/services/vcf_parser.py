def parse_vcf(lines):
    variants = []
    supported_gene_detected = False
    supported_genes = ["CYP2D6", "CYP2C19", "CYP2C9", "SLCO1B1", "TPMT", "DPYD"]

    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        cols = line.split("\t")
        if len(cols) < 8:
            continue  # skip malformed lines

        chrom, pos, id_, ref, alt, qual, filter_, info = cols[:8]

        info_dict = {}
        for field in info.split(";"):
            if "=" in field:
                key, value = field.split("=", 1)
                info_dict[key.upper()] = value

        gene = info_dict.get("GENE")
        star = info_dict.get("STAR", "*1/*1")
        rsid = info_dict.get("RS", "unknown")

        if gene in supported_genes:
            supported_gene_detected = True
            variants.append({
                "rsid": rsid,
                "chromosome": chrom,
                "position": int(pos),
                "ref": ref,
                "alt": alt,
                "gene": gene,
                "star": star
            })

    return variants, supported_gene_detected
