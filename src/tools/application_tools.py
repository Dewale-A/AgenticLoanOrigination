"""Tools for loan application processing."""

import json
from pathlib import Path
from typing import Optional, Type
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from src.config.settings import APPLICATIONS_DIR, MIN_CREDIT_SCORE, MAX_DTI_RATIO


class ApplicationLoaderInput(BaseModel):
    """Input for ApplicationLoaderTool."""
    application_id: Optional[str] = Field(
        default=None,
        description="Application ID to load. If not provided, lists all applications."
    )


class ApplicationLoaderTool(BaseTool):
    """Tool to load and parse loan applications."""
    
    name: str = "application_loader"
    description: str = """
    Loads loan application data from the applications directory.
    If application_id is provided, returns that specific application.
    If no application_id, returns a list of all available applications.
    Use this to get applicant information, loan details, and financial data.
    """
    args_schema: Type[BaseModel] = ApplicationLoaderInput
    
    def _run(self, application_id: Optional[str] = None) -> str:
        if application_id is None:
            return self._list_applications()
        return self._load_application(application_id)
    
    def _list_applications(self) -> str:
        apps = list(APPLICATIONS_DIR.glob("*.json"))
        if not apps:
            return "No applications found in the applications directory."
        
        app_list = []
        for app_file in apps:
            try:
                with open(app_file) as f:
                    data = json.load(f)
                app_list.append(f"- {data.get('application_id', app_file.stem)}: {data.get('applicant', {}).get('first_name', 'Unknown')} {data.get('applicant', {}).get('last_name', '')}")
            except:
                app_list.append(f"- {app_file.stem}: (unable to parse)")
        
        return f"Available applications:\\n" + "\\n".join(app_list)
    
    def _load_application(self, application_id: str) -> str:
        app_file = APPLICATIONS_DIR / f"{application_id}.json"
        if not app_file.exists():
            return f"Application {application_id} not found."
        
        with open(app_file) as f:
            data = json.load(f)
        
        return json.dumps(data, indent=2, default=str)


class CreditCheckInput(BaseModel):
    """Input for CreditCheckTool."""
    credit_score: int = Field(..., description="Applicant's credit score (300-850)")
    bankruptcies: int = Field(default=0, description="Number of bankruptcies")
    late_payments: int = Field(default=0, description="Late payments in last 12 months")


class CreditCheckTool(BaseTool):
    """Tool to perform credit evaluation."""
    
    name: str = "credit_check"
    description: str = """
    Evaluates an applicant's credit profile and determines creditworthiness.
    Takes credit score, bankruptcies, and late payments as input.
    Returns credit evaluation with risk factors and recommendations.
    """
    args_schema: Type[BaseModel] = CreditCheckInput
    
    def _run(self, credit_score: int, bankruptcies: int = 0, late_payments: int = 0) -> str:
        evaluation = {
            "credit_score": credit_score,
            "meets_minimum": credit_score >= MIN_CREDIT_SCORE,
            "credit_tier": self._get_credit_tier(credit_score),
            "risk_factors": [],
            "positive_factors": []
        }
        
        # Analyze credit
        if credit_score >= 750:
            evaluation["positive_factors"].append("Excellent credit score")
        elif credit_score >= 700:
            evaluation["positive_factors"].append("Good credit score")
        elif credit_score >= 650:
            evaluation["risk_factors"].append("Fair credit score - higher risk")
        else:
            evaluation["risk_factors"].append("Poor credit score - high risk")
        
        if bankruptcies > 0:
            evaluation["risk_factors"].append(f"{bankruptcies} bankruptcy(ies) on record")
        else:
            evaluation["positive_factors"].append("No bankruptcies")
        
        if late_payments > 2:
            evaluation["risk_factors"].append(f"{late_payments} late payments in last year")
        elif late_payments == 0:
            evaluation["positive_factors"].append("Perfect payment history")
        
        return json.dumps(evaluation, indent=2)
    
    def _get_credit_tier(self, score: int) -> str:
        if score >= 750:
            return "EXCELLENT"
        elif score >= 700:
            return "GOOD"
        elif score >= 650:
            return "FAIR"
        elif score >= 620:
            return "POOR"
        else:
            return "SUBPRIME"


class DTICalculatorInput(BaseModel):
    """Input for DTICalculatorTool."""
    annual_income: float = Field(..., description="Annual income")
    monthly_debt_payments: float = Field(..., description="Total monthly debt payments")
    proposed_loan_payment: float = Field(default=0, description="Proposed new loan monthly payment")


class DTICalculatorTool(BaseTool):
    """Tool to calculate debt-to-income ratio."""
    
    name: str = "dti_calculator"
    description: str = """
    Calculates debt-to-income (DTI) ratio for loan underwriting.
    Takes annual income, current monthly debts, and proposed loan payment.
    Returns DTI analysis with pass/fail status based on lending guidelines.
    """
    args_schema: Type[BaseModel] = DTICalculatorInput
    
    def _run(self, annual_income: float, monthly_debt_payments: float, proposed_loan_payment: float = 0) -> str:
        monthly_income = annual_income / 12
        
        current_dti = monthly_debt_payments / monthly_income if monthly_income > 0 else 0
        proposed_dti = (monthly_debt_payments + proposed_loan_payment) / monthly_income if monthly_income > 0 else 0
        
        result = {
            "monthly_income": round(monthly_income, 2),
            "current_monthly_debt": monthly_debt_payments,
            "proposed_payment": proposed_loan_payment,
            "current_dti": round(current_dti * 100, 2),
            "proposed_dti": round(proposed_dti * 100, 2),
            "max_allowed_dti": MAX_DTI_RATIO * 100,
            "passes_dti_check": proposed_dti <= MAX_DTI_RATIO,
            "dti_assessment": self._assess_dti(proposed_dti)
        }
        
        return json.dumps(result, indent=2)
    
    def _assess_dti(self, dti: float) -> str:
        if dti <= 0.20:
            return "Excellent - very low debt burden"
        elif dti <= 0.35:
            return "Good - manageable debt level"
        elif dti <= 0.43:
            return "Acceptable - at upper limit"
        else:
            return "Too high - exceeds maximum threshold"
