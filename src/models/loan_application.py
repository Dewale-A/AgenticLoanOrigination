"""Loan application data models."""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import date
from enum import Enum


class LoanPurpose(str, Enum):
    PERSONAL = "personal"
    DEBT_CONSOLIDATION = "debt_consolidation"
    HOME_IMPROVEMENT = "home_improvement"
    MAJOR_PURCHASE = "major_purchase"
    OTHER = "other"


class EmploymentStatus(str, Enum):
    EMPLOYED = "employed"
    SELF_EMPLOYED = "self_employed"
    RETIRED = "retired"
    UNEMPLOYED = "unemployed"


class Applicant(BaseModel):
    """Applicant personal information."""
    first_name: str
    last_name: str
    date_of_birth: date
    ssn_last_four: str = Field(..., min_length=4, max_length=4)
    email: str
    phone: str
    address: str
    city: str
    state: str
    zip_code: str


class EmploymentInfo(BaseModel):
    """Employment information."""
    status: EmploymentStatus
    employer_name: Optional[str] = None
    job_title: Optional[str] = None
    years_employed: float = 0
    monthly_income: float


class FinancialInfo(BaseModel):
    """Financial information."""
    credit_score: int = Field(..., ge=300, le=850)
    annual_income: float
    monthly_debt_payments: float
    bank_account_balance: float
    existing_loans: int = 0
    bankruptcies: int = 0
    late_payments_last_year: int = 0


class LoanApplication(BaseModel):
    """Complete loan application."""
    application_id: str
    application_date: date
    
    # Loan details
    loan_purpose: LoanPurpose
    requested_amount: float
    requested_term_months: int
    
    # Applicant info
    applicant: Applicant
    employment: EmploymentInfo
    financials: FinancialInfo
    
    # Calculated fields
    debt_to_income_ratio: Optional[float] = None
    
    def calculate_dti(self) -> float:
        """Calculate debt-to-income ratio."""
        monthly_income = self.financials.annual_income / 12
        if monthly_income > 0:
            self.debt_to_income_ratio = self.financials.monthly_debt_payments / monthly_income
        return self.debt_to_income_ratio or 0
