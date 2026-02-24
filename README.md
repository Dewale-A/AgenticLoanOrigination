# 🏦 Agentic Loan Origination

A production-ready **multi-agent AI system** for automated loan origination and underwriting. Built with [CrewAI](https://crewai.com), this system demonstrates how autonomous AI agents can collaborate to process loan applications through a complete underwriting workflow.

## 🏗️ System Architecture

<div align="center">
  <img src="docs/architecture.svg" alt="System Architecture" width="100%"/>
</div>

## 🎯 Overview

This system automates the loan origination process using 6 specialized AI agents that work together sequentially, mimicking a real lending institution's workflow:

```
┌────────────────────────────────────────────────────────────────────────────┐
│                    AGENTIC LOAN ORIGINATION SYSTEM                         │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│   📄 APPLICATION          🔍 VERIFICATION         📊 CREDIT                │
│   ┌─────────────┐        ┌─────────────┐        ┌─────────────┐            │
│   │  Document   │───────▶│ Verification│───────▶│   Credit    │            │
│   │   Intake    │        │   Analyst   │        │   Analyst   │            │
│   └─────────────┘        └─────────────┘        └─────────────┘            │
│         │                       │                      │                   │
│         │                       │                      ▼                   │
│         │                       │               ┌─────────────┐            │
│         │                       │               │    Risk     │            │
│         │                       │               │  Assessor   │            │
│         │                       │               └─────────────┘            │
│         │                       │                      │                   │
│         │                       ▼                      ▼                   │
│         │               ┌─────────────────────────────────┐                │
│         │               │       UNDERWRITER               │                │
│         │               │   (Final Decision Authority)    │                │
│         │               └─────────────────────────────────┘                │
│         │                              │                                   │
│         │                              ▼                                   │
│         │                       ┌─────────────┐                            │
│         └──────────────────────▶│    Offer    │                            │
│                                 │  Generator  │                            │
│                                 └─────────────┘                            │
│                                        │                                   │
│                                        ▼                                   │
│                              ┌─────────────────┐                           │
│                              │  LOAN DECISION  │                           │
│                              │  ✓ Approved     │                           │
│                              │  ⚠ Conditional  │                           │
│                              │  ✗ Denied       │                           │
│                              └─────────────────┘                           │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

## 🤖 Agent Roles

| Agent | Role | Tools |
|-------|------|-------|
| **Document Intake** | Loads and organizes application data | `application_loader` |
| **Verification** | Validates applicant information | `application_loader` |
| **Credit Analyst** | Evaluates creditworthiness | `credit_check`, `dti_calculator` |
| **Risk Assessor** | Calculates comprehensive risk scores | `risk_scoring` |
| **Underwriter** | Makes final approval decisions | `risk_scoring` |
| **Offer Generator** | Structures loan terms and pricing | `loan_pricing` |

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- OpenAI API key

### Installation

```bash
# Clone the repository
git clone https://github.com/Dewale-A/AgenticLoanOrigination.git
cd AgenticLoanOrigination

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### Running the System

```bash
# List available applications
python main.py --list

# Process a specific application
python main.py APP001

# Interactive mode
python main.py
```

## 📁 Project Structure

```
AgenticLoanOrigination/
├── main.py                 # Entry point
├── requirements.txt        # Dependencies
├── .env.example           # Environment template
├── applications/          # Loan application JSONs
│   ├── APP001.json       # Strong applicant (expect: APPROVED)
│   ├── APP002.json       # Moderate risk (expect: CONDITIONAL)
│   └── APP003.json       # High risk (expect: DENIED)
├── output/               # Decision reports
├── src/
│   ├── agents/
│   │   └── loan_agents.py    # Agent definitions
│   ├── tasks/
│   │   └── loan_tasks.py     # Task definitions
│   ├── tools/
│   │   ├── application_tools.py   # Intake & credit tools
│   │   └── underwriting_tools.py  # Risk & pricing tools
│   ├── models/
│   │   ├── loan_application.py    # Input data models
│   │   └── loan_decision.py       # Output data models
│   ├── config/
│   │   └── settings.py       # System configuration
│   └── crew.py              # Crew orchestration
└── tests/                   # Unit tests
```

## ⚙️ Configuration

Key settings in `.env`:

```bash
OPENAI_API_KEY=sk-...          # Required
OPENAI_MODEL=gpt-4o-mini       # Model selection
MIN_CREDIT_SCORE=620           # Minimum acceptable score
MAX_DTI_RATIO=0.43             # Maximum debt-to-income
BASE_INTEREST_RATE=7.5         # Starting rate for pricing
```

## 📊 Sample Applications

The system includes 3 sample applications demonstrating different outcomes:

| ID | Applicant | Credit Score | DTI | Expected Decision |
|----|-----------|--------------|-----|-------------------|
| APP001 | Sarah Mitchell | 742 | ~19% | ✅ APPROVED |
| APP002 | Marcus Johnson | 658 | ~32% | ⚠️ CONDITIONAL |
| APP003 | David Chen | 598 | ~35% | ❌ DENIED |

## 🔧 Extending the System

### Adding New Loan Products
Edit `src/config/settings.py`:
```python
LOAN_PRODUCTS = {
    "AUTO": {"min_amount": 5000, "max_amount": 75000, "max_term": 72},
    # Add your product...
}
```

### Adding New Tools
Create tools in `src/tools/` following the `BaseTool` pattern:
```python
from crewai.tools import BaseTool

class MyTool(BaseTool):
    name: str = "my_tool"
    description: str = "What it does"
    
    def _run(self, param: str) -> str:
        # Implementation
        return result
```

## 🏗️ Architecture Decisions

- **CrewAI Framework**: Provides robust agent orchestration with tool support
- **Sequential Process**: Ensures proper information flow between agents
- **Pydantic Models**: Type-safe data validation throughout the pipeline
- **Modular Tools**: Each tool is single-purpose and testable

## 📈 Future Enhancements

- [ ] External credit bureau API integration
- [ ] Document upload and OCR processing
- [ ] Real-time fraud detection agent
- [ ] Regulatory compliance checker
- [ ] Multi-product recommendation engine
- [ ] Portfolio risk analytics dashboard

## 📜 License

MIT License - see [LICENSE](LICENSE) for details.

## 👤 Author

**Dewale A** - Data & AI Governance Professional
- GitHub: [@Dewale-A](https://github.com/Dewale-A)
- LinkedIn: [Connect](https://linkedin.com/in/dewale-a)

---

*Built as part of a portfolio demonstrating autonomous multi-agent systems for financial services.*
