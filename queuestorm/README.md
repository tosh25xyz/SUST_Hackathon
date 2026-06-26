# QueueStorm Investigator

QueueStorm Investigator is a production-ready REST API service designed as an AI-powered customer support ticket investigator and router for digital financial platforms (like bKash). It accepts a customer complaint and their recent transaction history, utilizes Claude AI via the Anthropic API to classify, investigate, and route the ticket, and validates responses through custom programmatic safety post-processors.

---

## Tech Stack
- **Python 3.11+**
- **FastAPI** (High-performance web framework for APIs)
- **Uvicorn** (ASGI server implementation)
- **Anthropic SDK** (For integration with Claude models)
- **Pydantic v2** (For robust data validation and serialization)
- **python-dotenv** (For environment configuration management)
- **Docker** (For clean, isolated containerization)

---

## Setup & Running Locally

### 1. Prerequisites
Make sure you have Python 3.11+ installed.

### 2. Installation
Clone or navigate to the project directory and install dependencies:
```bash
# Navigate to the project root
cd queuestorm

# Create a virtual environment
python -m venv .venv
# Activate virtual environment
# On Windows (PowerShell):
.venv\Scripts\Activate.ps1
# On Linux/macOS:
source .venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### 3. Configuration
Copy the `.env.example` to `.env` and fill in your Anthropic API Key:
```bash
cp .env.example .env
```
Inside `.env`:
```env
ANTHROPIC_API_KEY=your_actual_anthropic_api_key_here
PORT=8000
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
```

### 4. Running the Server
Run the FastAPI development server:
```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```
The server will start at `http://127.0.0.1:8000`. You can inspect the interactive OpenAPI documentation at `http://127.0.0.1:8000/docs`.

---

## Running with Docker

### 1. Build the Docker Image
```bash
docker build -t queuestorm-investigator .
```

### 2. Run the Container
Run the container, passing your API Key as an environment variable:
```bash
docker run -p 8000:8000 --env ANTHROPIC_API_KEY="your_actual_key_here" queuestorm-investigator
```
The service will be accessible at `http://localhost:8000`.

---

## API Endpoints

### 1. Health Check
* **GET** `/health`
* **Response**: `{"status": "ok"}`
* **Response SLA**: Within 60 seconds of start.

### 2. Analyze Ticket
* **POST** `/analyze-ticket`
* **Response SLA**: Within 30 seconds.
* **Content-Type**: `application/json`

#### Request JSON Body Example:
```json
{
  "ticket_id": "TKT-001",
  "complaint": "I sent 5000 taka to a wrong number around 2pm today",
  "language": "en",
  "channel": "in_app_chat",
  "user_type": "customer",
  "campaign_context": "boishakh_bonanza_day_1",
  "transaction_history": [
    {
      "transaction_id": "TXN-9101",
      "timestamp": "2026-04-14T14:08:22Z",
      "type": "transfer",
      "amount": 5000.0,
      "counterparty": "+8801719876543",
      "status": "completed"
    }
  ],
  "metadata": {}
}
```

#### Response JSON Body Example:
```json
{
  "ticket_id": "TKT-001",
  "relevant_transaction_id": "TXN-9101",
  "evidence_verdict": "consistent",
  "case_type": "wrong_transfer",
  "severity": "high",
  "department": "dispute_resolution",
  "agent_summary": "Customer mistakenly sent 5000 BDT to (+8801719876543) via a completed transfer.",
  "recommended_next_action": "Contact the counterparty to request dispute resolution and initiate wrong transfer protocols.",
  "customer_reply": "We have recorded your issue regarding the transfer of 5000 BDT to +8801719876543. Any eligible amount will be returned through official channels if verified.",
  "human_review_required": true,
  "confidence": 0.95,
  "reason_codes": ["TXN_MATCHED", "DISPUTED_TRANSFER"]
}
```

---

## AI Implementation & Architecture

### Model Selection: `claude-sonnet-4-6` (Claude 3.5 Sonnet)
* **Model ID Used**: `claude-3-5-sonnet-20241022`
* **Why Chosen**: Claude 3.5 Sonnet represents the industry standard for reasoning, complex instructions following, and structured output formatting. In customer support, it excels at multilingual processing (English, Bangla, and mixed/Banglish) and can understand subtle details in transaction logs and complaints. It has a high context window and outputs exceptionally clean JSON schemas.

### Reasoning Flow
1. **Pydantic Validation**: Validates the request schema.
2. **Context Packaging**: Formats the ticket metadata and transaction logs using structured tags to supply clear boundaries to Claude.
3. **Structured Instruction System**: System prompts specify the classification enums and department routing rules.
4. **Retry on Parse Failure**: If the LLM generates a response that is malformed JSON or fails Pydantic schema validation, the analyzer retries once with a stricter system prompt. If it fails a second time, a safe, non-blocking fallback response is generated.

---

## Safety Logic & Post-Processing (safety.py)

We implement a multi-layer safety framework to protect customers and maintain absolute control:

### 1. Pre-Filtering (Prompt Injection Defense)
* Before sending anything to Claude, the customer's complaint is scanned for prompt injection attacks (such as instructions to "ignore previous instructions", "you are now a...", "system:").
* If detected, the API immediately bypasses Claude, marks the case as `phishing_or_social_engineering` / `fraud_risk` / `critical` / `human_review_required = True`, and returns a safe canned response.

### 2. Post-Processing Post-LLM Filters
After Claude responds, the raw result is sanitized:
* **Credential Protection (Rule 1)**: If `customer_reply` contains sensitive terms (PIN, OTP, password, card number), it is overwritten with a secure, standard response, and flagged for human review.
* **Conditional Assurances (Rule 2)**: Replaces absolute confirmations of refunds, reversals, or unblocking (e.g., *"we will refund you"*) with conditional, legally safe wording (e.g., *"any eligible amount will be returned through official channels if verified"*).
* **Link & Contact Safety (Rule 3)**: Scans replies for unofficial URLs, emails, or phone numbers. If found, replaces them with standard official hotline guidance (Helpline 16247).
* **Deterministic Routing Safeguards**: Overrides the department programmatically based on the case type to guarantee that no classification ever bypasses the required business routing rules.

---

## MODELS
- **Model**: claude-sonnet-4-6
- **Provider**: Anthropic API
- **Why chosen**: Strong multilingual support (Bangla/Banglish), reliable structured JSON output, fast response under 30s, no GPU required
- **Runs**: Remotely via Anthropic API

---

## Known Limitations
- Depends on Anthropic API availability
- Bangla language accuracy depends on Claude multilingual capability  
- No access to real transaction database — analyzes only what is provided in the request
- Cannot execute actual refunds or reversals — copilot only, all actions require human authorization

---

## Testing via Curl Command

```bash
curl -X POST http://localhost:8000/analyze-ticket \
  -H "Content-Type: application/json" \
  -d '{
    "ticket_id": "TKT-001",
    "complaint": "I sent 5000 taka to a wrong number around 2pm today",
    "language": "en",
    "channel": "in_app_chat",
    "user_type": "customer",
    "campaign_context": "boishakh_bonanza_day_1",
    "transaction_history": [
      {
        "transaction_id": "TXN-9101",
        "timestamp": "2026-04-14T14:08:22Z",
        "type": "transfer",
        "amount": 5000,
        "counterparty": "+8801719876543",
        "status": "completed"
      }
    ]
  }'
```
