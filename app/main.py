from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from datetime import datetime
from app.schemas import *
from app.vcf_parser import parse_vcf

app = FastAPI(title="PharmaGuard API")

templates = Jinja2Templates(directory="templates")

SUPPORTED_DRUGS = [
    "CODEINE",
    "WARFARIN",
    "CLOPIDOGREL",
    "SIMVASTATIN",
    "AZATHIOPRINE",
    "FLUOROURACIL"
]


# ------------------------------
# Risk Engine
# ------------------------------
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


# ------------------------------
# Web Home Page
# ------------------------------
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# ------------------------------
# API Endpoint (Swagger)
# ------------------------------
@app.post("/analyze", response_model=PharmaGuardResponse)
async def analyze(
    file: UploadFile = File(...),
    drug: str = Form(...)
):
    drug = drug.upper()

    if not file.filename.endswith(".vcf"):
        raise HTTPException(status_code=400, detail="Only VCF files allowed")

    if drug not in SUPPORTED_DRUGS:
        raise HTTPException(status_code=400, detail="Unsupported drug")

    contents = await file.read()

    if len(contents) > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File exceeds 5MB limit")

    file_text = contents.decode("utf-8")

    variants = parse_vcf(file_text)

    if not variants:
        raise HTTPException(status_code=400, detail="No variants found")

    first_variant = variants[0]

    risk_label, severity = simple_risk_engine(
        drug,
        first_variant["gene"],
        first_variant["star"]
    )

    return PharmaGuardResponse(
        patient_id="PATIENT_001",
        drug=drug,
        timestamp=datetime.utcnow(),
        risk_assessment={
            "risk_label": risk_label,
            "confidence_score": 0.85,
            "severity": severity
        },
        pharmacogenomic_profile={
            "primary_gene": first_variant["gene"],
            "diplotype": first_variant["star"],
            "phenotype": "Unknown",
            "detected_variants": [{
                "rsid": first_variant["rsid"],
                "chromosome": first_variant["chromosome"],
                "position": first_variant["position"],
                "genotype": first_variant["genotype"]
            }]
        },
        clinical_recommendation={
            "recommended_action": "Refer to CPIC guideline"
        },
        llm_generated_explanation={
            "summary": f"Variant in {first_variant['gene']} with allele {first_variant['star']} impacts {drug} metabolism."
        },
        quality_metrics={
            "vcf_parsing_success": True
        }
    )


# ------------------------------
# Web UI Endpoint
# ------------------------------
@app.post("/analyze_web", response_class=HTMLResponse)
async def analyze_web(
    request: Request,
    file: UploadFile = File(...),
    drug: str = Form(...)
):
    # Call existing API function
    result = await analyze(file, drug)

    return templates.TemplateResponse(
        "result.html",
        {
            "request": request,
            "result": result
        }
    )
