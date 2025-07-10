# PII Redaction Tool
## 🧩 Overview
### Purpose
This application automatically detects and redacts **Personally Identifiable Information (PII)** from customer interactions.

Designed for:
- Customer support teams needing to remove sensitive data from tickets
- Data engineers and analysts preparing datasets
- Privacy and compliance officers ensuring GDPR/PII protection

Why use it:
- Automates PII redaction
- Integrates with internal systems via modular connectors
- Uses LLMs for flexible, accurate detection
- Reduces compliance risk (e.g., GDPR, CCPA)

### 🛡️ GDPR Context
PII (**Personally Identifiable Information**) refers to any data that can be used — either alone or in combination with other information — to identify, contact, or locate an individual.

Examples of PII:
- *Direct identifiers:* Full name, social security number, driver’s license number, passport number, email address, phone number, date of birth.
- *Indirect identifiers:* IP addresses, device identifiers, biometric data, credit card and bank account numbers.
- *Other sensitive data:* Medical information, criminal history, citizenship or immigration status, ethnicity, or religious affiliation.

*PII redaction* is the process of detecting and removing (or masking) this data in order to protect privacy and reduce exposure to sensitive information leaks.

Why redaction matters under *GDPR*:
- ✅ Protect individuals' privacy and prevent unauthorized access to personal data.
- ✅ Support data minimization, keeping only the data that's truly necessary.
- ✅ Reduce risk when data is shared, stored, or processed—especially by third parties or internal teams not authorized to access PII.

## ⚙️ Functionality

###  General Workflow (System-to-System Integration)
1. Customer interactions — such as support tickets, messages, chats or emails — are stored in a connected data source (e.g., CRM, analytics platform, or internal database).
2. The app retrieves ticket data via a pre-configured API connector, using a unique ticket ID.
Multiple connectors can be supported simultaneously, making the app easily extendable.
3. The app analyzes the ticket content, detects any PII, and applies redaction according to the configured strategy.
4. The redacted ticket is then pushed back to the original system, replacing the unredacted version.

###  CRM-Agent Workflow (Manual Trigger via Webhook)
1. A support agent opens a ticket in the CRM and clicks a pre-configured "Redact PII" button.
2. This button triggers a webhook to the app, passing the ticket ID and CRM source.
3. The app fetches the ticket, scans for PII, and performs redaction. 
In some cases (like with Zendesk integration) redaction executed on the CRM level, the app should only detect PIIs.
4. The ticket content is updated in the CRM with the redacted version.

### LLM Agent
The main 'decision making' module of the app is an PII-identifying agent - the LLM-agent built using Google ADK framework - which requires access to Google API.
I used the cheapest available `gemini-1.5-flash` LLM-model that seems to sufficient for such task.

However, Google ADK alows to use [different models](https://google.github.io/adk-docs/agents/models/).


###  Redaction Strategies

The app supports multiple redaction strategies to handle detected PII.  

| Strategy   | Description                                                                 | Example Output                        |
|------------|-----------------------------------------------------------------------------|---------------------------------------|
| `mask`     | Replaces every character in the PII span with a `*`.                        | `Email: ********************`         |
| `tokenize` | Replaces the PII with a structured placeholder that includes the type.      | `Email: [PII::email]`                 |
| `hash`     | Replaces the PII with a hashed version (useful for anonymized comparisons). | `Email: 6f8db599de986fab7a21625b7916589c` |

ℹ️ **Default strategy:** `mask`

## 🔌 Creating and Using Connectors (General workflow)

To integrate with a new CRM or data platform, implement a connector module that defines two functions:
```python

def fetch_ticket(source: str, ticket_id: str) -> Ticket: ...
def update_ticket(source: str, redacted_ticket: RedactedTicket) -> None: ...


```
Requirements:
- The connector must reside in `connectors/` directory and be registered in `connector_registry.py`:

```python
_CONNECTORS = {
    "test": "app.connectors.test_crm_connector",
    "zendesk":  "app.connectors.zendesk_crm_connector",
    "salesforce": "app.connectors.zendesk_crm_connector",
}
```
- The source string passed to the app (e.g. "zendesk", "test") is used to route to the correct connector.

A test/mock connector  is included out of the box under `connectors/test_crm_connector.py`. This allows testing the system end-to-end without any real data source
Test connector uses local file as a tickets database example located `connectors/test_db.json`
You can use it by sending this payload to the `/ticket/test/{ticket_id}` endpoint.

## 🔌 Using Zendesk connector [CRM-Agent Workflow]

## 🛠️ Tech Details
### Project Structure
```text
📂 app/
│
├── main.py                         # FastAPI entry point and routes
│
├── requirements.txt                # Python dependencies
├── .env                            # Environment variables (e.g., API keys)
├── README.md                       # Project documentation
│
├── 📂 config/                      # App-level configurations
│   └── logger_config.py            # Logger setup and format
│
├── 📂 models/                             
│   └── pydentic_models.py          # Pydentic data models
│
├── 📂 agents/                      # Google ADK LLM agent(s)
│   ├── pii_detector_agent.py       # LLM interface for identifying PII
│   ├── pii_detector_runner.py      # Runner to initialize the agent
│   └── prompts.py                  # Prompt templates for LLM
│
├── 📂 connectors/                  # API connectors
│   ├── connector_registry.py       # Register/load external service connectors
│   ├── test_crm_connector.py       # Example CRM connector
│   └── mock_db.json                # Test local DB data
│
├── 📂 services/                    # Core logic and business services
│   └── redaction_service.py        # Main workflow: fetch, detect, redact, update
│
└── 📂 utils/                      # Utility functions
    ├── markdown_stripper.py        # Clean markdown artifacts from LLM output
    ├── pii_redactor.py             # Redaction logic
    └── pii_spans_locator.py        # Identify spans in the text for redaction
```


### Stack
- 🐍 Python v3.13
- 🚀 FastAPI 
- 🤖 Google ADK (Agent Development Kit) v1.5.0
### Versions
#### Curent Version
v.1.0.0 (10 Jul)

## 🚀 Setup & Deployment

### Prerequisites

Make sure you have the following installed on your system:

* **Python 3.13**
* **pip** (Python package installer)
* **Git** (to clone the repository)
* **Virtual environment support** (`venv`)
- (Optional) **Docker**

#### Getting google API key (for LLM agent setup)
Go to the [Google API Console](https://aistudio.google.com/apikey).

---

### Clone the Repository

```bash
git clone https://github.com/PSavvateev/pii-redaction-tool.git
cd pii-redaction-tool
```

---

### Create Virtual Environment

Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate      # On Linux/Mac
venv\Scripts\activate         # On Windows
```

---

### Install Dependencies

Install the required packages from `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

### Environment Variables

Create a `.env` file in the project root. You can start from the provided `.env.example`:

```bash
cp .env.example .env
```

Edit the `.env` file with your configuration:

```env
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_API_KEY=your_google_api_key_here

FAST_API_KEY=your_api_key_here
REDACTION_STRATEGY=mask

```
* `GOOGLE_GENAI_USE_VERTEXAI=FALSE`:
* `GOOGLE_API_KEY`:
* `FAST_API_KEY`: you can create any complex enough key to secure API access to the FastAPI application.
* `REDACTION_STRATEGY`: redaction mode — one of `mask`, `tokenize`, or `hash`.


---

### Run the App Locally

To start the FastAPI app locally:

```bash
uvicorn app.main:app --reload
```

It will be available at [http://localhost:8000](http://localhost:8000).

---

### Optional: Run with Docker

1. Build the Docker image:

```bash

docker build -t pii-redaction-tool .

```

2. Run the container:

```bash

docker run -p 8000:8000 --env-file .env pii-redaction-tool

```

### Run a Test Request (Optional)

Use `curl` or Postman to simulate an incoming webhook:

```bash
curl -X POST http://localhost:8000/ticket \
     -H "x-api-key: your_api_key_here" \
     -H "Content-Type: application/json" \
     -d '{
           "source": "zendesk",
           "ticket_id": 101
         }'
```

---



