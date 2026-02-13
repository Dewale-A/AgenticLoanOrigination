"""Configuration settings for the Loan Origination System."""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
APPLICATIONS_DIR = Path(os.getenv("APPLICATIONS_DIR", BASE_DIR / "applications"))
OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", BASE_DIR / "output"))

APPLICATIONS_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# LLM Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# Lending Parameters
MIN_CREDIT_SCORE = int(os.getenv("MIN_CREDIT_SCORE", 620))
MAX_DTI_RATIO = float(os.getenv("MAX_DTI_RATIO", 0.43))
MIN_INCOME = float(os.getenv("MIN_INCOME", 30000))
BASE_INTEREST_RATE = float(os.getenv("BASE_INTEREST_RATE", 7.5))

# Risk Tiers
RISK_TIERS = {
    "EXCELLENT": {"min_score": 750, "rate_adjustment": -1.5},
    "GOOD": {"min_score": 700, "rate_adjustment": -0.5},
    "FAIR": {"min_score": 650, "rate_adjustment": 1.0},
    "POOR": {"min_score": 620, "rate_adjustment": 2.5},
}

# Loan Products
LOAN_PRODUCTS = {
    "PERSONAL": {"min_amount": 1000, "max_amount": 50000, "max_term": 60},
    "DEBT_CONSOLIDATION": {"min_amount": 5000, "max_amount": 100000, "max_term": 84},
    "HOME_IMPROVEMENT": {"min_amount": 2500, "max_amount": 75000, "max_term": 72},
}

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
