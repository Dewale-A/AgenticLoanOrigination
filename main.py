#!/usr/bin/env python3
"""
Agentic Loan Origination System
===============================
A multi-agent AI system for automated loan processing and underwriting.

Usage:
    python main.py [application_id]
    
Examples:
    python main.py APP001      # Process a specific application
    python main.py --list      # List available applications
    python main.py             # Interactive mode
"""

import sys
import json
from datetime import datetime
from pathlib import Path

from src.crew import process_loan_application
from src.config.settings import APPLICATIONS_DIR, OUTPUT_DIR


def list_applications():
    """List all available loan applications."""
    apps = list(APPLICATIONS_DIR.glob("*.json"))
    
    if not apps:
        print("\nNo applications found in the applications directory.")
        print(f"Add JSON application files to: {APPLICATIONS_DIR}")
        return []
    
    print("\n" + "="*60)
    print("  AVAILABLE LOAN APPLICATIONS")
    print("="*60)
    
    app_ids = []
    for app_file in sorted(apps):
        try:
            with open(app_file) as f:
                data = json.load(f)
            app_id = data.get('application_id', app_file.stem)
            app_ids.append(app_id)
            applicant = data.get('applicant', {})
            name = f"{applicant.get('first_name', 'Unknown')} {applicant.get('last_name', '')}"
            amount = data.get('loan_request', {}).get('amount', 0)
            credit = data.get('financial_info', {}).get('credit_score', 'N/A')
            print(f"\n  [{app_id}]")
            print(f"    Applicant: {name}")
            print(f"    Amount: ${amount:,.2f}")
            print(f"    Credit Score: {credit}")
        except Exception as e:
            print(f"\n  [{app_file.stem}] - Error reading: {e}")
    
    print("\n" + "="*60)
    return app_ids


def save_output(application_id: str, result: str):
    """Save the processing result to a file."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = OUTPUT_DIR / f"{application_id}_{timestamp}_decision.md"
    
    with open(output_file, "w") as f:
        f.write(f"# Loan Decision Report\n")
        f.write(f"**Application ID:** {application_id}\n")
        f.write(f"**Processed:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("---\n\n")
        f.write(str(result))
    
    print(f"\n📄 Decision saved to: {output_file}")
    return output_file


def main():
    """Main entry point."""
    print("\n" + "="*60)
    print("  🏦 AGENTIC LOAN ORIGINATION SYSTEM")
    print("  Multi-Agent AI for Automated Underwriting")
    print("="*60)
    
    # Handle command line arguments
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        
        if arg in ["--list", "-l"]:
            list_applications()
            return
        
        if arg in ["--help", "-h"]:
            print(__doc__)
            return
        
        # Process specific application
        application_id = arg
    else:
        # Interactive mode
        app_ids = list_applications()
        
        if not app_ids:
            return
        
        print("\nEnter application ID to process (or 'q' to quit):")
        application_id = input("> ").strip()
        
        if application_id.lower() == 'q':
            print("Goodbye!")
            return
    
    # Verify application exists
    app_file = APPLICATIONS_DIR / f"{application_id}.json"
    if not app_file.exists():
        print(f"\n❌ Application '{application_id}' not found.")
        print(f"   Available applications are in: {APPLICATIONS_DIR}")
        return
    
    # Process the application
    print(f"\n🚀 Processing loan application: {application_id}")
    print("   This may take a minute as agents deliberate...\n")
    
    try:
        result = process_loan_application(application_id)
        
        # Save output
        save_output(application_id, result)
        
        print("\n" + "="*60)
        print("  FINAL DECISION")
        print("="*60)
        print(result)
        
    except Exception as e:
        print(f"\n❌ Error processing application: {e}")
        raise


if __name__ == "__main__":
    main()
