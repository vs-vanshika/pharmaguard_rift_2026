from pydantic import BaseModel
from typing import List
from datetime import datetime


class Variant(BaseModel):
    rsid: str
    chromosome: str
    position: int
    genotype: str


class PharmacogenomicProfile(BaseModel):
    primary_gene: str
    diplotype: str
    phenotype: str
    detected_variants: List[Variant]


class RiskAssessment(BaseModel):
    risk_label: str
    confidence_score: float
    severity: str


class ClinicalRecommendation(BaseModel):
    recommended_action: str


class LLMExplanation(BaseModel):
    summary: str


class QualityMetrics(BaseModel):
    vcf_parsing_success: bool


class PharmaGuardResponse(BaseModel):
    patient_id: str
    drug: str
    timestamp: datetime
    risk_assessment: RiskAssessment
    pharmacogenomic_profile: PharmacogenomicProfile
    clinical_recommendation: ClinicalRecommendation
    llm_generated_explanation: LLMExplanation
    quality_metrics: QualityMetrics
