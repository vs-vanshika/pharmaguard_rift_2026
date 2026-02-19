from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import List
from datetime import datetime
import os

from app.schemas import PharmaGuardResponse
from app.vcf_parser import parse_vcf
from app.rule_engine import evaluate_risk
from app.llm_engine import generate_llm_explanation

# ✅ Create FastAPI app
app = FastAPI(title="PharmaGuard AI")

# ✅ Setup templates
templates = Jinja2Templates(directory="templates")


# ✅ Homepage Route
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# ✅ Analyze Endpoint
@app.post("/analyze", response_model=List[PharmaGuardResponse])
async def analyze(
    file: UploadFile = File(...),
    drug: str = Form(...)
):

    # Validate file extension
    if not file.filename.endswith(".vcf"):
        raise HTTPException(status_code=400, detail="Only VCF files allowed")

    contents = await file.read()

    # Validate file size (5MB limit)
    if len(contents) > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File exceeds 5MB limit")

    file_text = contents.decode("utf-8")
    variants = parse_vcf(file_text)

    if not variants:
        raise HTTPException(status_code=400, detail="No pharmacogenomic variants found")

    patient_id = os.path.splitext(file.filename)[0].upper()

    # Support comma-separated drugs
    drugs = [d.strip().upper() for d in drug.split(",")]

    responses = []

    for single_drug in drugs:

        # Get rule-based risk
        risk_data = evaluate_risk(single_drug, variants)

        # Call OpenAI (returns STRING)
        explanation_text = generate_llm_explanation(
            single_drug,
            risk_data["pharmacogenomic_profile"]["primary_gene"],
            risk_data["pharmacogenomic_profile"]["diplotype"],
            risk_data["risk_assessment"]["risk_label"]
        )

        # Build response
        response = PharmaGuardResponse(
            patient_id=patient_id,
            drug=single_drug,
            timestamp=datetime.utcnow().isoformat(),

            risk_assessment=risk_data["risk_assessment"],

            pharmacogenomic_profile=risk_data["pharmacogenomic_profile"],

            clinical_recommendation=risk_data["clinical_recommendation"],

            llm_generated_explanation={
                "summary": explanation_text
            },

            quality_metrics={
                "vcf_parsing_success": True
            }
        )

        responses.append(response)

    return responses
