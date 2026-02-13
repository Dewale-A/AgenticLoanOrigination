"""Loan decision data models."""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date
from enum import Enum


class DecisionStatus(str, Enum):
    APPROVED = "approved"
    DENIED = "denied"
    REFER = "refer_to_underwriter"
    PENDING = "pending_review"


class RiskLevel(str, Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    VERY_HIGH = "very_high"


class RiskAssessment(BaseModel):
    """Risk assessment results."""
    risk_score: float = Field(..., ge=0, le=100)
    risk_level: RiskLevel
    credit_risk_score: float
    income_risk_score: float
    dti_risk_score: float
    employment_risk_score: float
    
    risk_factors: List[str] = []
    positive_factors: List[str] = []
    
    recommendation: str


class LoanOffer(BaseModel):
    """Loan offer details."""
    approved_amount: float
    interest_rate: float
    term_months: int
    monthly_payment: float
    total_interest: float
    total_repayment: float
    apr: float
    
    conditions: List[str] = []


class LoanDecision(BaseModel):
    """Final loan decision."""
    application_id: str
    decision_date: date
    status: DecisionStatus
    
    # Assessment
    risk_assessment: Optional[RiskAssessment] = None
    
    # Offer (if approved)
    offer: Optional[LoanOffer] = None
    
    # Decision details
    decision_reasons: List[str] = []
    compliance_checks_passed: bool = True
    compliance_notes: List[str] = []
    
    # Underwriter notes
    underwriter_notes: str = ""
    
    def to_summary(self) -> str:
        """Generate decision summary."""
        summary = f"""
LOAN DECISION SUMMARY
=====================
Application ID: {self.application_id}
Decision Date: {self.decision_date}
Status: {self.status.value.upper()}

"""
        if self.risk_assessment:
            summary += f"""
RISK ASSESSMENT
---------------
Risk Score: {self.risk_assessment.risk_score}/100
Risk Level: {self.risk_assessment.risk_level.value}
Recommendation: {self.risk_assessment.recommendation}

Risk Factors:
{chr(10).join('- ' + f for f in self.risk_assessment.risk_factors) or '- None identified'}

Positive Factors:
{chr(10).join('- ' + f for f in self.risk_assessment.positive_factors) or '- None identified'}
"""

        if self.offer:
            summary += f"""
LOAN OFFER
----------
Approved Amount: ${self.offer.approved_amount:,.2f}
Interest Rate: {self.offer.interest_rate:.2f}%
Term: {self.offer.term_months} months
Monthly Payment: ${self.offer.monthly_payment:,.2f}
Total Interest: ${self.offer.total_interest:,.2f}
Total Repayment: ${self.offer.total_repayment:,.2f}
APR: {self.offer.apr:.2f}%

Conditions:
{chr(10).join('- ' + c for c in self.offer.conditions) or '- None'}
"""

        if self.decision_reasons:
            summary += f"""
DECISION REASONS
----------------
{chr(10).join('- ' + r for r in self.decision_reasons)}
"""

        return summary
