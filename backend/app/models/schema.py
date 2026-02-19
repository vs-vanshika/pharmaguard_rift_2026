from pydantic import BaseModel
from typing import List
from datetime import datetime


class Variant(BaseModel):
    rsid: str
    chromosome: str
    position: int
    ref: str
    alt: str

class RiskAssessment(BaseModel):
    risk_label: str
    confidence_score: float
    severity: str


class PharmacogenomicProfile(BaseModel):
    primary_gene: str
    diplotype: str
    phenotype: str
    detected_variants: List[Variant]


class ClinicalRecommendation(BaseModel):
    summary: str
    cpic_guideline_reference: str
    recommended_action: str


class LLMExplanation(BaseModel):
    summary: str
    mechanism: str
    variant_interpretation: str


class QualityMetrics(BaseModel):
    vcf_parsing_success: bool
    variants_found: int
    supported_gene_detected: bool


class AnalysisResponse(BaseModel):
    patient_id: str
    drug: str
    timestamp: datetime
    risk_assessment: RiskAssessment
    pharmacogenomic_profile: PharmacogenomicProfile
    clinical_recommendation: ClinicalRecommendation
    llm_generated_explanation: LLMExplanation
    quality_metrics: QualityMetrics
