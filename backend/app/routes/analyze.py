from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from datetime import datetime
from app.services.vcf_parser import parse_vcf
from app.services.phenotype_engine import determine_phenotype
from app.services.risk_engine import assess_risk, DRUG_GENE_MAP
from app.services.recommendation_engine import generate_recommendation
from app.services.llm_engine import generate_explanation
from app.models.schema import *
from typing import List
from enum import Enum

# Define drug enum for Swagger dropdown
class DrugEnum(str, Enum):
    CODEINE = "CODEINE"
    WARFARIN = "WARFARIN"
    CLOPIDOGREL = "CLOPIDOGREL"
    SIMVASTATIN = "SIMVASTATIN"
    AZATHIOPRINE = "AZATHIOPRINE"
    FLUOROURACIL = "FLUOROURACIL"

router = APIRouter()

@router.post("/analyze", response_model=List[AnalysisResponse])
async def analyze_vcf(
    file: UploadFile = File(...),
    drug: List[DrugEnum] = Form(...)
):
    # read file
    content = await file.read()
    lines = content.decode().split("\n")
    variants, supported_gene = parse_vcf(lines)

    results = []  # must be defined inside the function

    for d in drug:  # process each selected drug
        gene = DRUG_GENE_MAP.get(d.value, "Unknown")
        variant_for_gene = next((v for v in variants if v["gene"] == gene), None)
        star = variant_for_gene["star"] if variant_for_gene else "*1/*1"

        phenotype = determine_phenotype(gene, star)
        risk_label, confidence, severity = assess_risk(d.value, phenotype)
        rec_summary, cpic_ref, action = generate_recommendation(d.value, phenotype)
        llm_output = generate_explanation(d.value, gene, phenotype)

        results.append(
            AnalysisResponse(
                patient_id="PATIENT_001",
                drug=d.value,
                timestamp=datetime.utcnow(),
                risk_assessment=RiskAssessment(
                    risk_label=risk_label,
                    confidence_score=confidence,
                    severity=severity
                ),
                pharmacogenomic_profile=PharmacogenomicProfile(
                    primary_gene=gene,
                    diplotype=star,
                    phenotype=phenotype,
                    detected_variants=variants
                ),
                clinical_recommendation=ClinicalRecommendation(
                    summary=rec_summary,
                    cpic_guideline_reference=cpic_ref,
                    recommended_action=action
                ),
                llm_generated_explanation=LLMExplanation(**llm_output),
                quality_metrics=QualityMetrics(
                    vcf_parsing_success=len(variants) > 0,
                    variants_found=len(variants),
                    supported_gene_detected=supported_gene
                )
            )
        )

    return results  # ✅ must be inside the function
