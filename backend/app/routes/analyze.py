from fastapi import APIRouter, UploadFile, File, Form
from datetime import datetime
from app.services.vcf_parser import parse_vcf
from app.services.phenotype_engine import determine_phenotype
from app.services.risk_engine import assess_risk, DRUG_GENE_MAP
from app.services.recommendation_engine import generate_recommendation
from app.services.llm_engine import generate_explanation
from app.models.schema import *

router = APIRouter()


@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_vcf(
    file: UploadFile = File(...),
    drug: str = Form(...)
):
    content = await file.read()
    lines = content.decode().split("\n")

    variants, supported_gene = parse_vcf(lines)

    gene = DRUG_GENE_MAP.get(drug.upper(), "Unknown")

    diplotype = "*1/*2"
    phenotype = determine_phenotype(diplotype)

    risk_label, confidence, severity = assess_risk(drug, phenotype)

    rec_summary, cpic_ref, action = generate_recommendation(drug, phenotype)

    llm_output = generate_explanation(drug, gene, phenotype)

    return AnalysisResponse(
        patient_id="PATIENT_001",
        drug=drug.upper(),
        timestamp=datetime.utcnow(),
        risk_assessment=RiskAssessment(
            risk_label=risk_label,
            confidence_score=confidence,
            severity=severity
        ),
        pharmacogenomic_profile=PharmacogenomicProfile(
            primary_gene=gene,
            diplotype=diplotype,
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
            vcf_parsing_success=True,
            variants_found=len(variants),
            supported_gene_detected=supported_gene
        )
    )