"""Task definitions for the loan origination workflow."""

from crewai import Task, Agent


def create_intake_task(agent: Agent, application_id: str) -> Task:
    """Creates the document intake task."""
    return Task(
        description=f"""Load and review loan application {application_id}.
        
        Your responsibilities:
        1. Use the application_loader tool to load the application data
        2. Extract all key information: applicant details, loan request, financial info
        3. Identify any missing or incomplete fields
        4. Summarize the application for downstream processing
        
        Application ID: {application_id}
        """,
        expected_output="""A structured summary containing:
        - Applicant name and contact info
        - Loan amount requested and purpose
        - Annual income and employment details
        - Current debts and assets
        - List of any missing or flagged items""",
        agent=agent,
    )


def create_verification_task(agent: Agent, application_id: str) -> Task:
    """Creates the verification task."""
    return Task(
        description=f"""Verify the information in loan application {application_id}.
        
        Your responsibilities:
        1. Review the application data for consistency
        2. Verify income against employment information
        3. Check that all dates and figures are reasonable
        4. Flag any red flags or inconsistencies
        
        Note: In a production system, this would include external verification calls.
        For this PoC, perform logical verification of the provided data.
        """,
        expected_output="""A verification report containing:
        - Verification status (VERIFIED / NEEDS_REVIEW / FLAGGED)
        - Income verification summary
        - Employment verification summary
        - List of any discrepancies or concerns
        - Recommendation for proceeding""",
        agent=agent,
    )


def create_credit_analysis_task(agent: Agent) -> Task:
    """Creates the credit analysis task."""
    return Task(
        description="""Perform comprehensive credit analysis for this loan application.
        
        Your responsibilities:
        1. Use the credit_check tool with the applicant's credit score and history
        2. Use the dti_calculator tool to compute debt-to-income ratio
        3. Evaluate credit tier and identify risk factors
        4. Assess ability to take on the proposed loan payment
        
        Use the applicant information from the previous tasks.
        """,
        expected_output="""A credit analysis report containing:
        - Credit score evaluation and tier
        - Debt-to-income ratio (current and proposed)
        - Credit risk factors (positive and negative)
        - Credit recommendation (PASS / CONDITIONAL / FAIL)
        - Specific concerns or strengths to highlight""",
        agent=agent,
    )


def create_risk_assessment_task(agent: Agent) -> Task:
    """Creates the risk assessment task."""
    return Task(
        description="""Calculate the comprehensive risk score for this application.
        
        Your responsibilities:
        1. Use the risk_scoring tool with all relevant applicant data
        2. Review the credit analysis from the previous task
        3. Consider all risk factors holistically
        4. Provide risk-based recommendation
        
        Gather the required inputs from previous task outputs:
        - Credit score
        - DTI ratio
        - Annual income
        - Years employed
        - Any bankruptcies
        - Loan amount requested
        """,
        expected_output="""A risk assessment report containing:
        - Total risk score (0-100)
        - Risk level classification
        - Component score breakdown
        - Key risk factors identified
        - Risk-based recommendation
        - Approval likelihood percentage""",
        agent=agent,
    )


def create_underwriting_task(agent: Agent) -> Task:
    """Creates the underwriting decision task."""
    return Task(
        description="""Make the final underwriting decision for this loan application.
        
        Your responsibilities:
        1. Review all previous analyses (verification, credit, risk)
        2. Consider compensating factors that may offset weaknesses
        3. Make a final decision: APPROVED, APPROVED_WITH_CONDITIONS, or DENIED
        4. Document your reasoning clearly
        
        Apply sound underwriting judgment. Look for ways to approve loans
        when risk is manageable, but protect against undue risk.
        """,
        expected_output="""An underwriting decision containing:
        - DECISION: APPROVED / APPROVED_WITH_CONDITIONS / DENIED
        - Decision rationale (clear explanation)
        - Compensating factors considered
        - Conditions for approval (if applicable)
        - Maximum approved loan amount
        - Recommended loan term""",
        agent=agent,
    )


def create_offer_generation_task(agent: Agent) -> Task:
    """Creates the loan offer generation task."""
    return Task(
        description="""Generate the final loan offer for this approved application.
        
        Your responsibilities:
        1. Use the loan_pricing tool to calculate terms
        2. Structure a competitive offer based on risk profile
        3. Present clear, borrower-friendly terms
        4. Include all required disclosures
        
        Only generate an offer if the underwriting decision was APPROVED
        or APPROVED_WITH_CONDITIONS. If denied, summarize the denial.
        """,
        expected_output="""A loan offer document containing:
        - Loan amount
        - Interest rate and APR
        - Monthly payment
        - Loan term
        - Total interest over life of loan
        - Total amount to be repaid
        - Any conditions or requirements
        - Next steps for the borrower
        
        OR if denied:
        - Denial summary with primary reasons
        - Suggestions for improving creditworthiness""",
        agent=agent,
    )
