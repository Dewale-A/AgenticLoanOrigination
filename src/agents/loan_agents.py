"""Agent definitions for the loan origination system."""

from crewai import Agent, LLM

from src.config.settings import OPENAI_API_KEY, OPENAI_MODEL
from src.tools.application_tools import ApplicationLoaderTool, CreditCheckTool, DTICalculatorTool
from src.tools.underwriting_tools import RiskScoringTool, LoanPricingTool


# Initialize LLM
llm = LLM(
    model=f"openai/{OPENAI_MODEL}",
    api_key=OPENAI_API_KEY,
    temperature=0.3,
)

# Initialize tools
application_loader = ApplicationLoaderTool()
credit_check = CreditCheckTool()
dti_calculator = DTICalculatorTool()
risk_scoring = RiskScoringTool()
loan_pricing = LoanPricingTool()


def document_intake_agent() -> Agent:
    """Creates the Document Intake Agent."""
    return Agent(
        role="Document Intake Specialist",
        goal="Load and organize loan application documents, extracting all relevant data for processing",
        backstory="""You are an experienced document intake specialist at a lending institution. 
        Your job is to receive loan applications, ensure all required information is present,
        and organize the data for downstream processing. You're meticulous about details
        and flag any missing or inconsistent information immediately.""",
        tools=[application_loader],
        llm=llm,
        verbose=True,
    )


def verification_agent() -> Agent:
    """Creates the Verification Agent."""
    return Agent(
        role="Verification Analyst",
        goal="Verify applicant information including income, employment, and identity",
        backstory="""You are a verification analyst responsible for ensuring all applicant
        information is accurate and consistent. You cross-reference data points to identify
        discrepancies and flag potential fraud indicators. Your verification is crucial
        for making sound lending decisions.""",
        tools=[application_loader],
        llm=llm,
        verbose=True,
    )


def credit_analyst_agent() -> Agent:
    """Creates the Credit Analyst Agent."""
    return Agent(
        role="Senior Credit Analyst",
        goal="Analyze applicant creditworthiness and provide detailed credit assessment",
        backstory="""You are a senior credit analyst with over 10 years of experience 
        in consumer lending. You evaluate credit reports, payment histories, and 
        outstanding debts to determine creditworthiness. Your analysis forms the 
        foundation of lending decisions and you're known for thorough, balanced assessments.""",
        tools=[credit_check, dti_calculator],
        llm=llm,
        verbose=True,
    )


def risk_assessor_agent() -> Agent:
    """Creates the Risk Assessment Agent."""
    return Agent(
        role="Risk Assessment Specialist",
        goal="Calculate comprehensive risk scores and identify all risk factors",
        backstory="""You are a risk assessment specialist who evaluates loan applications
        using quantitative models and qualitative judgment. You consider credit metrics,
        income stability, employment history, and market conditions to produce accurate
        risk assessments that protect the institution while treating applicants fairly.""",
        tools=[risk_scoring],
        llm=llm,
        verbose=True,
    )


def underwriter_agent() -> Agent:
    """Creates the Underwriter Agent."""
    return Agent(
        role="Senior Loan Underwriter",
        goal="Make final credit decisions based on all available analysis",
        backstory="""You are a senior loan underwriter with authority to approve or deny
        loan applications. You review all analysis from credit and risk teams, weigh
        compensating factors, and make fair, defensible decisions. You balance risk
        management with customer service, looking for ways to approve good loans
        while protecting against defaults.""",
        tools=[risk_scoring],
        llm=llm,
        verbose=True,
    )


def offer_generator_agent() -> Agent:
    """Creates the Offer Generator Agent."""
    return Agent(
        role="Loan Structuring Specialist",
        goal="Structure approved loans with optimal terms for both lender and borrower",
        backstory="""You are a loan structuring specialist who designs loan offers
        for approved applications. You balance profitability with competitive pricing,
        ensuring rates and terms match the risk profile while remaining attractive
        to borrowers. You present clear, compliant loan offers that borrowers can
        easily understand.""",
        tools=[loan_pricing],
        llm=llm,
        verbose=True,
    )
