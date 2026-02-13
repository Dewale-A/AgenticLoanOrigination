"""Main crew orchestration for loan origination."""

from crewai import Crew, Process

from src.agents import (
    document_intake_agent,
    verification_agent,
    credit_analyst_agent,
    risk_assessor_agent,
    underwriter_agent,
    offer_generator_agent,
)
from src.tasks import (
    create_intake_task,
    create_verification_task,
    create_credit_analysis_task,
    create_risk_assessment_task,
    create_underwriting_task,
    create_offer_generation_task,
)


def create_loan_origination_crew(application_id: str) -> Crew:
    """
    Creates the loan origination crew with all agents and tasks.
    
    Args:
        application_id: The ID of the loan application to process
        
    Returns:
        Configured Crew ready to execute
    """
    # Initialize agents
    intake_agent = document_intake_agent()
    verifier = verification_agent()
    credit_analyst = credit_analyst_agent()
    risk_assessor = risk_assessor_agent()
    underwriter = underwriter_agent()
    offer_generator = offer_generator_agent()
    
    # Create tasks with dependencies
    intake_task = create_intake_task(intake_agent, application_id)
    verification_task = create_verification_task(verifier, application_id)
    credit_task = create_credit_analysis_task(credit_analyst)
    risk_task = create_risk_assessment_task(risk_assessor)
    underwriting_task = create_underwriting_task(underwriter)
    offer_task = create_offer_generation_task(offer_generator)
    
    # Set up task dependencies (context from previous tasks)
    verification_task.context = [intake_task]
    credit_task.context = [intake_task, verification_task]
    risk_task.context = [intake_task, credit_task]
    underwriting_task.context = [verification_task, credit_task, risk_task]
    offer_task.context = [intake_task, underwriting_task]
    
    # Create and return the crew
    crew = Crew(
        agents=[
            intake_agent,
            verifier,
            credit_analyst,
            risk_assessor,
            underwriter,
            offer_generator,
        ],
        tasks=[
            intake_task,
            verification_task,
            credit_task,
            risk_task,
            underwriting_task,
            offer_task,
        ],
        process=Process.sequential,
        verbose=True,
    )
    
    return crew


def process_loan_application(application_id: str) -> str:
    """
    Process a loan application through the full origination workflow.
    
    Args:
        application_id: The ID of the loan application to process
        
    Returns:
        Final loan decision and offer (or denial)
    """
    print(f"\n{'='*60}")
    print(f"  AGENTIC LOAN ORIGINATION SYSTEM")
    print(f"  Processing Application: {application_id}")
    print(f"{'='*60}\n")
    
    crew = create_loan_origination_crew(application_id)
    result = crew.kickoff()
    
    print(f"\n{'='*60}")
    print(f"  PROCESSING COMPLETE")
    print(f"{'='*60}\n")
    
    return result
