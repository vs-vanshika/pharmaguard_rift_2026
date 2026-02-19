from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from typing import List
import os

from app.schemas import PharmaGuardResponse
from app.vcf_parser import parse_vcf
from app.rule_engine import evaluate_risk
from app.llm_engine import generate_llm_explanation


app = FastAPI(
    title="PharmaGuard – AI Pharmacogenomics Platform",
    description="AI-powered precision medicine risk engine.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    swagger_ui_parameters={
        "defaultModelsExpandDepth": -1,
        "docExpansion": "none"
    }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")

SUPPORTED_DRUGS = [
    "CODEINE",
    "WARFARIN",
    "CLOPIDOGREL",
    "SIMVASTATIN",
    "AZATHIOPRINE",
    "FLUOROURACIL"
]


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/analyze", response_model=List[PharmaGuardResponse])
async def analyze(
    file: UploadFile = File(...),
    drug: List[str] = Form(...)
):

    if not file.filename.endswith(".vcf"):
        raise HTTPException(status_code=400, detail="Only VCF files allowed")

    contents = await file.read()

    if len(contents) > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File exceeds 5MB limit")

    file_text = contents.decode("utf-8")
    variants = parse_vcf(file_text)

    if not variants:
        raise HTTPException(status_code=400, detail="No pharmacogenomic variants found")

    patient_id = os.path.splitext(file.filename)[0].upper()

    processed_drugs = []
    for d in drug:
        if "," in d:
            processed_drugs.extend([x.strip().upper() for x in d.split(",")])
        else:
            processed_drugs.append(d.strip().upper())

    processed_drugs = list(set(processed_drugs))

    responses = []

    for single_drug in processed_drugs:

        if single_drug not in SUPPORTED_DRUGS:
            raise HTTPException(status_code=400, detail=f"Unsupported drug: {single_drug}")

        risk_data = evaluate_risk(single_drug, variants)

        explanation = generate_llm_explanation(
            single_drug,
            risk_data["gene"],
            risk_data["diplotype"],
            risk_data["risk_label"]
        )

        response = PharmaGuardResponse(
            patient_id=patient_id,
            drug=single_drug,
            timestamp=datetime.utcnow().isoformat(),
            risk_assessment=risk_data["risk_assessment"],
            pharmacogenomic_profile=risk_data["pharmacogenomic_profile"],
            clinical_recommendation=risk_data["clinical_recommendation"],
            llm_generated_explanation={"summary": explanation},
            quality_metrics={"vcf_parsing_success": True}
        )

        responses.append(response)

    return responses
