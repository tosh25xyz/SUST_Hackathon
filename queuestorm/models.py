from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

# --- Enums matching EXACTLY the specifications ---

class CaseType(str, Enum):
    wrong_transfer = "wrong_transfer"
    payment_failed = "payment_failed"
    refund_request = "refund_request"
    duplicate_payment = "duplicate_payment"
    merchant_settlement_delay = "merchant_settlement_delay"
    agent_cash_in_issue = "agent_cash_in_issue"
    phishing_or_social_engineering = "phishing_or_social_engineering"
    other = "other"

class Department(str, Enum):
    customer_support = "customer_support"
    dispute_resolution = "dispute_resolution"
    payments_ops = "payments_ops"
    merchant_operations = "merchant_operations"
    agent_operations = "agent_operations"
    fraud_risk = "fraud_risk"

class EvidenceVerdict(str, Enum):
    consistent = "consistent"
    inconsistent = "inconsistent"
    insufficient_data = "insufficient_data"

class Severity(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"

# --- Request Schemas ---

class TransactionEntry(BaseModel):
    transaction_id: str
    timestamp: str  # ISO 8601 format
    type: str  # "transfer" | "payment" | "cash_in" | "cash_out" | "settlement" | "refund"
    amount: float
    counterparty: str
    status: str  # "completed" | "failed" | "pending" | "reversed"

class TicketAnalysisRequest(BaseModel):
    ticket_id: str
    complaint: str
    language: Optional[str] = None  # "en" | "bn" | "mixed"
    channel: Optional[str] = None  # "in_app_chat" | "call_center" | "email" | "merchant_portal" | "field_agent"
    user_type: Optional[str] = None  # "customer" | "merchant" | "agent" | "unknown"
    campaign_context: Optional[str] = None
    transaction_history: Optional[List[TransactionEntry]] = None
    metadata: Optional[Dict[str, Any]] = None

# --- Response Schemas ---

class TicketAnalysisResponse(BaseModel):
    ticket_id: str
    relevant_transaction_id: Optional[str] = None
    evidence_verdict: EvidenceVerdict
    case_type: CaseType
    severity: Severity
    department: Department
    agent_summary: str
    recommended_next_action: str
    customer_reply: str
    human_review_required: bool
    confidence: float
    reason_codes: List[str]
