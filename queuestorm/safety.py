import re
from typing import Dict, Any, List

# --- Constants & Patterns ---

# Rule 1: Sensitive Credential Keywords
SENSITIVE_CREDENTIALS = ["PIN", "OTP", "password", "card number", "please share", "please provide your"]

# Rule 2: Absolute confirmation phrases
BAD_CONFIRMATIONS = [
    r"\bwe\s+will\s+refund\b",
    r"\bwe'll\s+refund\b",
    r"\brefund\s+will\s+be\s+processed\b",
    r"\byour\s+money\s+will\s+be\s+returned\b",
    r"\bwe'll\s+reverse\s+the\s+transaction\b",
    r"\bwe\s+will\s+reverse\s+the\s+transaction\b",
    r"\bwe'll\s+reverse\b",
    r"\bwe\s+will\s+reverse\b",
    r"\bwe\s+will\s+unblock\b",
    r"\bwe'll\s+unblock\b",
    # Bangla equivalents
    r"ফেরত\s+দেব",
    r"ফেরত\s+দেওয়া\s+হবে",
    r"রিফান্ড\s+করব",
    r"রিভার্স\s+করব",
    # Banglish equivalents
    r"refund\s+dibo",
    r"taka\s+ferot",
    r"reverse\s+korbo",
]

# Rule 3: Third-party contacts patterns
URL_PATTERN = re.compile(r"https?://\S+|www\.\S+|[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}\b", re.IGNORECASE)
EMAIL_PATTERN = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}", re.IGNORECASE)
# Matches numbers with 7 or more digits, but excludes official shortcode 16247
PHONE_PATTERN = re.compile(r"\b\d{7,15}\b")

OFFICIAL_HOTLINES = ["16247"]
OFFICIAL_DOMAINS = ["bkash.com", "queuestorm.com"]

# Rule 4: Prompt Injection Keywords
INJECTION_KEYWORDS = [
    r"ignore\s+(?:[a-zA-Z]+\s+)*instructions",
    r"ignore\s+previous",
    r"you\s+are\s+now",
    r"respond\s+only\s+with",
    r"system\s*:",
    r"forget\s+(?:your|my)?\s*instructions",
    r"override\s+(?:the)?\s*prompt",
    r"dan\s+mode",
    r"jailbreak",
    r"disregard\s+instructions",
    r"act\s+as",
]

# Fallbacks
SAFE_REPLY_CREDENTIALS = (
    "For your security, we will never ask for your PIN, OTP, password, card number, "
    "or sensitive account details. Your ticket has been routed to our team for manual review."
)
SAFE_CONFIRMATION_PHRASE = "any eligible amount will be returned through official channels if verified"
SAFE_REPLY_THIRD_PARTY = (
    "Please only contact us through our official support channel (helpline 16247 or in-app chat). "
    "Do not trust unofficial contact numbers or external links."
)

# --- Functions ---

def detect_prompt_injection(complaint: str) -> bool:
    """
    Checks if a complaint contains typical prompt injection signatures.
    """
    if not complaint:
        return True  # Treat empty complaint as suspicious/invalid
    
    for kw in INJECTION_KEYWORDS:
        if re.search(kw, complaint, re.IGNORECASE):
            return True
            
    return False

def generate_injection_response(ticket_id: str) -> Dict[str, Any]:
    """
    Generates a safe fallback response for a suspected prompt injection ticket.
    """
    return {
        "ticket_id": ticket_id,
        "relevant_transaction_id": None,
        "evidence_verdict": "insufficient_data",
        "case_type": "phishing_or_social_engineering",
        "severity": "critical",
        "department": "fraud_risk",
        "agent_summary": "Security alert: Suspicious complaint text resembling a prompt injection or override attempt.",
        "recommended_next_action": "Audit account for security violations and fraudulent activities.",
        "customer_reply": "We detected suspicious activity on this ticket. For security reasons, it has been flagged for manual investigation.",
        "human_review_required": True,
        "confidence": 1.0,
        "reason_codes": ["PROMPT_INJECTION_DETECTED"]
    }

def sanitize_customer_reply(reply: str) -> tuple[str, bool]:
    """
    Sanitizes customer_reply against credential leakage (Rule 1) and external contacts (Rule 3).
    Returns (sanitized_reply, was_flagged)
    """
    flagged = False
    
    # Remove safe warning phrases for checks to avoid false positives
    check_reply = reply
    check_reply = check_reply.replace("Please do not share your PIN or OTP with anyone.", "")
    check_reply = check_reply.replace("Please do not share your PIN or OTP with anyone", "")
    check_reply = check_reply.replace("অনুগ্রহ করে কারো সাথে আপনার পিন বা ওটিপি শেয়ার করবেন না।", "")
    check_reply = check_reply.replace("অনুগ্রহ করে কারো সাথে আপনার পিন বা ওটিপি শেয়ার করবেন না", "")
    check_reply = check_reply.replace("please share the transaction ID", "")
    check_reply = check_reply.replace("please share the transaction id", "")
    check_reply = check_reply.replace("Please share the transaction ID", "")
    check_reply = check_reply.replace("Please share the transaction id", "")
    
    # Rule 1: Credentials Check
    for word in SENSITIVE_CREDENTIALS:
        if word.lower() in check_reply.lower():
            reply = SAFE_REPLY_CREDENTIALS
            flagged = True
            break

    # Rule 3: Third-party contacts and links
    # Let's inspect URLs
    urls = URL_PATTERN.findall(reply)
    has_unauthorized_link = False
    for url in urls:
        # Check if the url contains any official domain
        if not any(domain in url.lower() for domain in OFFICIAL_DOMAINS):
            has_unauthorized_link = True
            break
            
    # Inspect emails
    emails = EMAIL_PATTERN.findall(reply)
    has_email = len(emails) > 0
    
    # Inspect phone numbers
    phones = PHONE_PATTERN.findall(reply)
    has_unauthorized_phone = False
    for phone in phones:
        if phone not in OFFICIAL_HOTLINES:
            has_unauthorized_phone = True
            break
            
    if has_unauthorized_link or has_email or has_unauthorized_phone:
        reply = SAFE_REPLY_THIRD_PARTY
        flagged = True

    return reply, flagged

def sanitize_certainty(text: str) -> tuple[str, bool]:
    """
    Sanitizes absolute confirmations of refunds/reversals/unblocks (Rule 2) in replies and next actions.
    Returns (sanitized_text, was_modified)
    """
    modified = False
    sanitized = text
    for pattern in BAD_CONFIRMATIONS:
        # Replace occurrences with the safe conditional phrase
        if re.search(pattern, sanitized, re.IGNORECASE):
            sanitized = re.sub(pattern, SAFE_CONFIRMATION_PHRASE, sanitized, flags=re.IGNORECASE)
            modified = True
    return sanitized, modified

def enforce_routing_rules(case_type: str, severity: str, original_department: str) -> str:
    """
    Guarantees strict department routing logic based on case_type and severity.
    """
    if case_type == "wrong_transfer":
        return "dispute_resolution"
    elif case_type in ("payment_failed", "duplicate_payment"):
        return "payments_ops"
    elif case_type == "merchant_settlement_delay":
        return "merchant_operations"
    elif case_type == "agent_cash_in_issue":
        return "agent_operations"
    elif case_type == "phishing_or_social_engineering":
        return "fraud_risk"
    elif case_type == "refund_request":
        # wrong_transfer, contested refund_request -> dispute_resolution
        # other, low severity refund_request, vague cases -> customer_support
        if severity == "low":
            return "customer_support"
        else:
            return "dispute_resolution"
    elif case_type == "other":
        return "customer_support"
    
    return original_department

def post_process_sanitize(response_dict: Dict[str, Any]) -> Dict[str, Any]:
    """
    Applies all post-processing sanitization, safety adjustments, and routing checks.
    """
    # 1. Enforce department routing logic programmatically
    orig_dept = response_dict.get("department", "customer_support")
    case_type = response_dict.get("case_type", "other")
    severity = response_dict.get("severity", "medium")
    
    corrected_dept = enforce_routing_rules(case_type, severity, orig_dept)
    response_dict["department"] = corrected_dept
    
    # 2. Sanitize customer reply (Rule 1 & 3)
    original_reply = response_dict.get("customer_reply", "")
    sanitized_reply, flagged_reply = sanitize_customer_reply(original_reply)
    response_dict["customer_reply"] = sanitized_reply
    if flagged_reply:
        response_dict["human_review_required"] = True
        if "SAFETY_VIOLATION_FLAGGED" not in response_dict.setdefault("reason_codes", []):
            response_dict["reason_codes"].append("SAFETY_VIOLATION_FLAGGED")
            
    # 3. Sanitize certainty in customer reply and recommended next action (Rule 2)
    sanitized_reply_cert, modified_reply_cert = sanitize_certainty(response_dict["customer_reply"])
    response_dict["customer_reply"] = sanitized_reply_cert
    
    original_action = response_dict.get("recommended_next_action", "")
    sanitized_action, modified_action = sanitize_certainty(original_action)
    response_dict["recommended_next_action"] = sanitized_action
    
    if modified_reply_cert or modified_action:
        if "CERTAINTY_SANITIZED" not in response_dict.setdefault("reason_codes", []):
            response_dict["reason_codes"].append("CERTAINTY_SANITIZED")
            
    # 4. Human review triggers
    # Set human_review_required = true for disputes, suspicious cases, high/critical severity, ambiguous evidence.
    # We only override to True if it is phishing, a safety violation, or if the analyzer didn't set it.
    # Otherwise, we trust the analyzer/simulator's judgment (e.g. for automatic reversals or clarification requests).
    if response_dict.get("human_review_required") is None:
        if (
            severity in ("high", "critical")
            or case_type in ("wrong_transfer", "phishing_or_social_engineering")
            or response_dict.get("evidence_verdict") in ("inconsistent", "insufficient_data")
        ):
            response_dict["human_review_required"] = True
    else:
        if case_type == "phishing_or_social_engineering" or flagged_reply:
            response_dict["human_review_required"] = True
        
    return response_dict
