from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from datetime import datetime
from app.schemas import PharmaGuardResponse
from app.vcf_parser import parse_vcf

app = FastAPI(title="PharmaGuard API")


SUPPORTED_DRUGS = [
    "CODEINE",
    "WARFARIN",
    "CLOPIDOGREL",
    "SIMVASTATIN",
    "AZATHIOPRINE",
    "FLUOROURACIL"
]


DRUG_GENE_MAP = {
    "CODEINE": "CYP2D6",
    "WARFARIN": "CYP2C9",
    "CLOPIDOGREL": "CYP2C19",
    "SIMVASTATIN": "SLCO1B1",
    "AZATHIOPRINE": "TPMT",
    "FLUOROURACIL": "DPYD"
}


def simple_risk_engine(drug: str, gene: str, star: str):
    risk_label = "Safe"
    severity = "none"

    if drug == "CODEINE" and gene == "CYP2D6" and star == "*4":
        risk_label = "Ineffective"
        severity = "high"

    if drug == "WARFARIN" and gene == "CYP2C9" and star == "*3":
        risk_label = "Toxic"
        severity = "critical"

    if drug == "CLOPIDOGREL" and gene == "CYP2C19" and star == "*2":
        risk_label = "Ineffective"
        severity = "high"

    if drug == "SIMVASTATIN" and gene == "SLCO1B1" and star == "*5":
        risk_label = "Toxic"
        severity = "high"

    if drug == "AZATHIOPRINE" and gene == "TPMT":
        risk_label = "Toxic"
        severity = "critical"

    if drug == "FLUOROURACIL" and gene == "DPYD":
        risk_label = "Toxic"
        severity = "critical"

    return risk_label, severity


@app.post("/analyze", response_model=PharmaGuardResponse)
async def analyze(
    file: UploadFile = File(...),
    drug: str = Form(...)
):

    if not file.filename.endswith(".vcf"):
        raise HTTPException(status_code=400, detail="Only VCF files allowed")

    contents = await file.read()

    if len(contents) > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File exceeds 5MB limit")

    file_text = contents.decode("utf-8")

    variants = parse_vcf(file_text)

    if not variants:
        raise HTTPException(status_code=400, detail="No variants found")

    drug = drug.upper()

    if drug not in SUPPORTED_DRUGS:
        raise HTTPException(status_code=400, detail="Unsupported drug")

    required_gene = DRUG_GENE_MAP.get(drug)

    matching_variant = next(
        (v for v in variants if v["gene"] == required_gene),
        None
    )

    if matching_variant:
        risk_label, severity = simple_risk_engine(
            drug,
            matching_variant["gene"],
            matching_variant["star"]
        )

        detected_variants = [{
            "rsid": matching_variant["rsid"],
            "chromosome": matching_variant["chromosome"],
            "position": matching_variant["position"],
            "genotype": matching_variant["genotype"]
        }]

        diplotype = matching_variant["star"]
    else:
        risk_label = "Unknown"
        severity = "none"
        detected_variants = []
        diplotype = "Unknown"

    return {
        "patient_id": "PATIENT_001",
        "drug": drug,
        "timestamp": datetime.utcnow().isoformat(),
        "risk_assessment": {
            "risk_label": risk_label,
            "confidence_score": 0.90,
            "severity": severity
        },
        "pharmacogenomic_profile": {
            "primary_gene": required_gene,
            "diplotype": diplotype,
            "phenotype": "Unknown",
            "detected_variants": detected_variants
        },
        "clinical_recommendation": {
            "recommended_action": "Refer to CPIC guideline"
        },
        "llm_generated_explanation": {
            "summary": f"Variant in {required_gene} influences {drug} metabolism and may require clinical consideration."
        },
        "quality_metrics": {
            "vcf_parsing_success": True
        }
    }
