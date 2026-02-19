import json
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RULES_DIR = os.path.join(BASE_DIR, "rules")

with open(os.path.join(RULES_DIR, "drug_guidelines.json")) as f:
    clinical_rules = json.load(f)

with open(os.path.join(RULES_DIR, "phenotype_rules.json")) as f:
    phenotype_map = json.load(f)


PHENOTYPE_ABBREV = {
    "Poor Metabolizer": "PM",
    "Intermediate Metabolizer": "IM",
    "Normal Metabolizer": "NM",
    "Rapid Metabolizer": "RM",
    "Ultra Rapid Metabolizer": "UM",
    "Decreased Function": "IM",
    "Normal Function": "NM"
}


def evaluate_risk(drug: str, variants: list):

    for v in variants:
        gene = v["gene"]
        star = v["star"]

        raw_pheno = phenotype_map.get(gene, {}).get(star, "Unknown")
        phenotype = PHENOTYPE_ABBREV.get(raw_pheno, "Unknown")

        rule = clinical_rules.get(drug, {}).get(gene, {}).get(raw_pheno)

        if rule:
            risk_label = rule["risk_label"]

            if risk_label not in ["Safe", "Adjust Dosage", "Toxic"]:
                risk_label = "Adjust Dosage"

            return {
                "gene": gene,
                "diplotype": star,
                "risk_label": risk_label,
                "risk_assessment": {
                    "risk_label": risk_label,
                    "confidence_score": 0.95,
                    "severity": rule["severity"]
                },
                "pharmacogenomic_profile": {
                    "primary_gene": gene,
                    "diplotype": star,
                    "phenotype": phenotype,
                    "detected_variants": [{
                        "rsid": v["rsid"],
                        "chromosome": v["chromosome"],
                        "position": v["position"],
                        "genotype": v["genotype"]
                    }]
                },
                "clinical_recommendation": {
                    "recommended_action": rule["recommendation"]
                }
            }

    return {
        "gene": "Unknown",
        "diplotype": "Unknown",
        "risk_label": "Unknown",
        "risk_assessment": {
            "risk_label": "Unknown",
            "confidence_score": 0.6,
            "severity": "none"
        },
        "pharmacogenomic_profile": {
            "primary_gene": "Unknown",
            "diplotype": "Unknown",
            "phenotype": "Unknown",
            "detected_variants": []
        },
        "clinical_recommendation": {
            "recommended_action": "Insufficient pharmacogenomic evidence."
        }
    }
