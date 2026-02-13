"""Tools for loan underwriting and pricing."""

import json
from typing import Type
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from src.config.settings import BASE_INTEREST_RATE, RISK_TIERS, MIN_CREDIT_SCORE, MAX_DTI_RATIO


class RiskScoringInput(BaseModel):
    """Input for RiskScoringTool."""
    credit_score: int = Field(..., description="Credit score (300-850)")
    dti_ratio: float = Field(..., description="Debt-to-income ratio as decimal (e.g., 0.35)")
    annual_income: float = Field(..., description="Annual income")
    years_employed: float = Field(..., description="Years at current job")
    bankruptcies: int = Field(default=0, description="Number of bankruptcies")
    loan_amount: float = Field(..., description="Requested loan amount")


class RiskScoringTool(BaseTool):
    """Tool to calculate risk score for loan applications."""
    
    name: str = "risk_scoring"
    description: str = """
    Calculates a comprehensive risk score (0-100) for a loan application.
    Takes credit score, DTI ratio, income, employment history, and loan amount.
    Returns risk score, risk level, and detailed breakdown of risk factors.
    Lower scores = lower risk = better for approval.
    """
    args_schema: Type[BaseModel] = RiskScoringInput
    
    def _run(
        self,
        credit_score: int,
        dti_ratio: float,
        annual_income: float,
        years_employed: float,
        bankruptcies: int,
        loan_amount: float
    ) -> str:
        # Calculate component scores (0-25 each, lower = better)
        credit_risk = self._score_credit(credit_score)
        dti_risk = self._score_dti(dti_ratio)
        income_risk = self._score_income(annual_income, loan_amount)
        employment_risk = self._score_employment(years_employed)
        
        # Bankruptcy penalty
        bankruptcy_penalty = min(bankruptcies * 15, 30)
        
        # Total risk score (0-100)
        total_risk = min(credit_risk + dti_risk + income_risk + employment_risk + bankruptcy_penalty, 100)
        
        result = {
            "total_risk_score": round(total_risk, 1),
            "risk_level": self._get_risk_level(total_risk),
            "components": {
                "credit_risk": round(credit_risk, 1),
                "dti_risk": round(dti_risk, 1),
                "income_risk": round(income_risk, 1),
                "employment_risk": round(employment_risk, 1),
                "bankruptcy_penalty": bankruptcy_penalty
            },
            "recommendation": self._get_recommendation(total_risk, credit_score, dti_ratio),
            "approval_likelihood": self._get_approval_likelihood(total_risk)
        }
        
        return json.dumps(result, indent=2)
    
    def _score_credit(self, score: int) -> float:
        if score >= 750:
            return 5
        elif score >= 700:
            return 10
        elif score >= 650:
            return 18
        elif score >= 620:
            return 23
        else:
            return 25
    
    def _score_dti(self, dti: float) -> float:
        if dti <= 0.20:
            return 5
        elif dti <= 0.30:
            return 10
        elif dti <= 0.36:
            return 15
        elif dti <= 0.43:
            return 20
        else:
            return 25
    
    def _score_income(self, income: float, loan_amount: float) -> float:
        ratio = loan_amount / income if income > 0 else 999
        if ratio <= 0.25:
            return 5
        elif ratio <= 0.50:
            return 10
        elif ratio <= 0.75:
            return 15
        elif ratio <= 1.0:
            return 20
        else:
            return 25
    
    def _score_employment(self, years: float) -> float:
        if years >= 5:
            return 5
        elif years >= 2:
            return 10
        elif years >= 1:
            return 18
        else:
            return 25
    
    def _get_risk_level(self, score: float) -> str:
        if score <= 25:
            return "LOW"
        elif score <= 50:
            return "MODERATE"
        elif score <= 75:
            return "HIGH"
        else:
            return "VERY_HIGH"
    
    def _get_recommendation(self, risk_score: float, credit_score: int, dti: float) -> str:
        if credit_score < MIN_CREDIT_SCORE:
            return "DENY - Credit score below minimum"
        if dti > MAX_DTI_RATIO:
            return "DENY - DTI exceeds maximum"
        if risk_score <= 35:
            return "APPROVE - Strong application"
        elif risk_score <= 55:
            return "APPROVE WITH CONDITIONS"
        elif risk_score <= 75:
            return "REFER TO SENIOR UNDERWRITER"
        else:
            return "DENY - High risk"
    
    def _get_approval_likelihood(self, risk_score: float) -> str:
        if risk_score <= 30:
            return "Very High (90%+)"
        elif risk_score <= 45:
            return "High (70-89%)"
        elif risk_score <= 60:
            return "Moderate (50-69%)"
        elif risk_score <= 75:
            return "Low (25-49%)"
        else:
            return "Very Low (<25%)"


class LoanPricingInput(BaseModel):
    """Input for LoanPricingTool."""
    loan_amount: float = Field(..., description="Approved loan amount")
    term_months: int = Field(..., description="Loan term in months")
    credit_tier: str = Field(..., description="Credit tier: EXCELLENT, GOOD, FAIR, or POOR")
    risk_level: str = Field(..., description="Risk level: LOW, MODERATE, HIGH")


class LoanPricingTool(BaseTool):
    """Tool to calculate loan pricing and terms."""
    
    name: str = "loan_pricing"
    description: str = """
    Calculates loan pricing including interest rate, monthly payment, and total cost.
    Takes loan amount, term, credit tier, and risk level.
    Returns complete loan offer with payment schedule details.
    """
    args_schema: Type[BaseModel] = LoanPricingInput
    
    def _run(
        self,
        loan_amount: float,
        term_months: int,
        credit_tier: str,
        risk_level: str
    ) -> str:
        # Calculate interest rate
        base_rate = BASE_INTEREST_RATE
        
        # Credit tier adjustment
        tier_adjustment = RISK_TIERS.get(credit_tier, {}).get("rate_adjustment", 0)
        
        # Risk level adjustment
        risk_adjustments = {"LOW": -0.5, "MODERATE": 0.5, "HIGH": 1.5, "VERY_HIGH": 3.0}
        risk_adjustment = risk_adjustments.get(risk_level, 0)
        
        final_rate = base_rate + tier_adjustment + risk_adjustment
        final_rate = max(final_rate, 5.0)  # Floor rate
        
        # Calculate monthly payment (amortization formula)
        monthly_rate = final_rate / 100 / 12
        if monthly_rate > 0:
            monthly_payment = loan_amount * (monthly_rate * (1 + monthly_rate)**term_months) / ((1 + monthly_rate)**term_months - 1)
        else:
            monthly_payment = loan_amount / term_months
        
        total_repayment = monthly_payment * term_months
        total_interest = total_repayment - loan_amount
        
        # APR (simplified - same as rate for this example)
        apr = final_rate
        
        result = {
            "loan_amount": loan_amount,
            "term_months": term_months,
            "interest_rate": round(final_rate, 2),
            "apr": round(apr, 2),
            "monthly_payment": round(monthly_payment, 2),
            "total_interest": round(total_interest, 2),
            "total_repayment": round(total_repayment, 2),
            "rate_breakdown": {
                "base_rate": base_rate,
                "credit_adjustment": tier_adjustment,
                "risk_adjustment": risk_adjustment
            },
            "first_payment_interest": round(loan_amount * monthly_rate, 2),
            "first_payment_principal": round(monthly_payment - (loan_amount * monthly_rate), 2)
        }
        
        return json.dumps(result, indent=2)
