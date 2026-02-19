import os
import random

OUTPUT_DIR = "sample_vcf1"
NUM_PATIENTS = 100  # 50 is enough for hackathon

os.makedirs(OUTPUT_DIR, exist_ok=True)

genes = {
    "CYP2D6": {
        "rsids": ["rs3892097"],
        "stars": ["*1", "*4"]
    },
    "CYP2C19": {
        "rsids": ["rs4244285"],
        "stars": ["*1", "*2"]
    },
    "CYP2C9": {
        "rsids": ["rs1057910"],
        "stars": ["*1", "*3"]
    },
    "SLCO1B1": {
        "rsids": ["rs4149056"],
        "stars": ["*1", "*5"]
    },
    "TPMT": {
        "rsids": ["rs1142345"],
        "stars": ["*1", "*3A"]
    },
    "DPYD": {
        "rsids": ["rs3918290"],
        "stars": ["*1", "*2A"]
    }
}

def generate_variant(gene):
    rsid = random.choice(genes[gene]["rsids"])
    star = random.choice(genes[gene]["stars"])
    chrom = random.randint(1, 22)
    pos = random.randint(10000000, 200000000)
    genotype = random.choice(["0/1", "1/1"])

    return f"{chrom}\t{pos}\t{rsid}\tA\tG\t.\tPASS\tGENE={gene};STAR={star}\tGT\t{genotype}"

for i in range(1, NUM_PATIENTS + 1):
    filename = os.path.join(OUTPUT_DIR, f"patient_{i:03}.vcf")

    with open(filename, "w") as f:
        f.write("##fileformat=VCFv4.2\n")
        f.write('##INFO=<ID=GENE,Number=1,Type=String,Description="Gene Symbol">\n')
        f.write('##INFO=<ID=STAR,Number=1,Type=String,Description="Star Allele">\n')
        f.write('##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">\n')
        f.write("#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tSAMPLE\n")

        selected_genes = random.sample(list(genes.keys()), random.randint(1, 3))

        for gene in selected_genes:
            f.write(generate_variant(gene) + "\n")

print(f" Generated {NUM_PATIENTS} synthetic VCF files in '{OUTPUT_DIR}'")
