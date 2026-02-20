# PharmaGuard: Pharmacogenomic Risk Prediction System

**Track:** HealthTech / Pharmacogenomics / Explainable AI  
**Hackathon:** RIFT 2026  

---

##  Live Demo

Access the deployed application here: [Live Demo URL](https://your-render-app-url.com)

---

##  LinkedIn Demo Video

Watch our 2–5 min project demonstration: [LinkedIn Video Link](https://www.linkedin.com/posts/your-demo-link)  
*Remember to tag RIFT official page and use hashtags:*  
`#RIFT2026 #PharmaGuard #Pharmacogenomics #AIinHealthcare`

---

## Architecture Overview

PharmaGuard is a **FastAPI-based backend** with a web interface for uploading **VCF files** and selecting **pharmacogenomic drugs**. It performs:

1. **VCF Parsing:** Extracts variants with `GENE`, `STAR`, `RS` annotations.  
2. **Phenotype Prediction:** Determines patient drug metabolizer status (e.g., PM, IM, NM).  
3. **Risk Assessment:** Evaluates drug-specific risks (Safe, Adjust Dosage, Toxic, Ineffective, Unknown).  
4. **Clinical Recommendation:** Provides actionable guidance aligned with **CPIC guidelines**.  
5. **LLM-generated Explanation:** Explains the genetic mechanism and dosing reasoning using OpenAI GPT models.

**Flow Diagram :**  

+-----------------+       +----------------+       +----------------+
|   VCF Upload    |  -->  | VCF Parser     |  -->  | Phenotype &    |
|  (Drag & Drop)  |       | (extract GENE, |       | Risk Engine    |
|                 |       | STAR, RS)      |       | (CPIC-aligned)|
+-----------------+       +----------------+       +----------------+
                                                    |
                                                    v
                                         +-----------------------+
                                         | Recommendation Engine |
                                         |  & LLM Explanation    |
                                         +-----------------------+
                                                    |
                                                    v
                                         +-----------------------+
                                         |  JSON Output & UI     |
                                         |  Risk, Phenotype,     |
                                         |  Clinical Advice      |
                                         +-----------------------+

---

## Tech Stack

- **Backend:** Python 3.12, FastAPI, Uvicorn  
- **Frontend / API UI:** FastAPI Swagger UI  
- **LLM:** OpenAI GPT-4o-mini  
- **Deployment:** Render (Web Service)  
- **Version Control:** Git + GitHub  

---

## Installation Instructions

**1. Clone repository**
git clone https://github.com/vs-vanshika/pharmaguard_rift_2026.git
cd pharmaguard_rift_2026/backend

**2. Create virtual environment**

python -m venv venv
venv\Scripts\activate  # Windows
# OR
source venv/bin/activate  # macOS/Linux

**3. Install Dependencies**

pip install -r requirements.txt

**4. Add environment variables**

cp .env.example .env
Add your OpenAI key:

OPENAI_API_KEY=your_openai_api_key

**5. Run Locally**

uvicorn app.main:app --reload

##API Documentation
POST /analyze

Description: Upload a .vcf file and select one or multiple drugs to get a pharmacogenomic risk report.

Request:

file: VCF file (.vcf)

drug: List of supported drugs (CODEINE, WARFARIN, CLOPIDOGREL, SIMVASTATIN, AZATHIOPRINE, FLUOROURACIL)

Response: JSON following this schema:

{
  "patient_id": "PATIENT_001",
  "drug": "DRUG_NAME",
  "timestamp": "ISO8601_timestamp",
  "risk_assessment": {
    "risk_label": "Safe|Adjust Dosage|Toxic|Ineffective|Unknown",
    "confidence_score": 0.0,
    "severity": "none|low|moderate|high|critical"
  },
  "pharmacogenomic_profile": {
    "primary_gene": "GENE_SYMBOL",
    "diplotype": "*X/*Y",
    "phenotype": "PM|IM|NM|RM|URM|Unknown",
    "detected_variants": [
      { "rsid": "rsXXXX", "chromosome": "X", "position": 123456, "genotype": "0/1" }
    ]
  },
  "clinical_recommendation": {
    "recommended_action": "..."
  },
  "llm_generated_explanation": {
    "summary": "..."
  },
  "quality_metrics": {
    "vcf_parsing_success": true
  }
}


## Usage Examples

Open Swagger UI at /docs.

Upload test1.vcf or any valid VCF file.

Select one or multiple drugs from the dropdown.

Click Execute → view JSON output with risk, phenotype, recommendation, and explanation.



## Sample VCF Files

backend/sample_vcfs/test1.vcf

backend/sample_vcfs/test2.vcf

Ensure VCF follows standard structure with INFO tags: GENE, STAR, RS.

##Team Members

Snehal S Juvekar
Sowmya A
Vanshika S(Team Leader)
Varshini Smitha S
