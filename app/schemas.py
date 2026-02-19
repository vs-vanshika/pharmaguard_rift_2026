from pydantic import BaseModel
from typing import List


class DetectedVariant(BaseModel):
    rsid: str
    chromosome: str
    position: int
    genotype: str


class RiskAssessment(BaseModel):
    risk_label: str
    confidence_score: float
    severity: str


class PharmacogenomicProfile(BaseModel):
    primary_gene: str
    diplotype: str
    phenotype: str
    detected_variants: List[DetectedVariant]


class ClinicalRecommendation(BaseModel):
    recommended_action: str


class LLMGeneratedExplanation(BaseModel):
    summary: str


class QualityMetrics(BaseModel):
    vcf_parsing_success: bool


class PharmaGuardResponse(BaseModel):
    patient_id: str
    drug: str
    timestamp: str
    risk_assessment: RiskAssessment
    pharmacogenomic_profile: PharmacogenomicProfile
    clinical_recommendation: ClinicalRecommendation
    llm_generated_explanation: LLMGeneratedExplanation
    quality_metrics: QualityMetrics
