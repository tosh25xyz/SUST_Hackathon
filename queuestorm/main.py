import os
import json
import logging
from fastapi import FastAPI, Request, status, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from dotenv import load_dotenv

# Load environment variables first
load_dotenv()

# Setup logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("queuestorm.main")

from models import TicketAnalysisRequest, TicketAnalysisResponse
import safety
import analyzer

app = FastAPI(
    title="QueueStorm Investigator",
    description="Fintech AI support copilot backend",
    version="1.0.0"
)

# --- Exception Handlers ---

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Distinguishes between malformed input (JSON syntax error -> 400) 
    and semantically invalid input (Pydantic validation failure -> 422).
    """
    errors = exc.errors()
    logger.warning(f"Request validation failure: {errors}")
    
    # Check if this error is caused by body parsing or json decoding
    is_malformed = False
    for err in errors:
        err_type = err.get("type", "").lower()
        err_loc = err.get("loc", [])
        # If it's a JSON parsing/decoding issue or body is entirely missing/malformed
        if "json" in err_type or "decode" in err_type or "parsing" in err_type or ("body" in err_loc and len(err_loc) == 1):
            is_malformed = True
            break
            
    if is_malformed:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "Malformed JSON input. Please verify JSON syntax."}
        )
        
    # Semantically invalid parameters
    error_details = []
    for err in errors:
        loc = " -> ".join(str(l) for l in err["loc"] if l != "body")
        error_details.append({
            "field": loc or "root",
            "message": err["msg"],
            "type": err["type"]
        })
        
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Semantically invalid input. One or more fields failed validation checks.",
            "errors": error_details
        }
    )

@app.exception_handler(json.JSONDecodeError)
async def json_decode_exception_handler(request: Request, exc: json.JSONDecodeError):
    """
    Returns 400 when json.loads fails (e.g. from custom middleware or manual body reading).
    """
    logger.warning(f"JSON decode failure: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": "Malformed JSON input. Please verify JSON syntax."}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """
    Catches all other unhandled exceptions and returns a clean 500 error.
    Strictly avoids exposing stack traces, API keys, or secrets.
    """
    logger.exception("Unhandled application exception:")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An internal server error occurred while processing your request."}
    )

# --- Routes ---

@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """
    Uptime health check endpoint.
    """
    return {"status": "ok"}

@app.post("/analyze-ticket", response_model=TicketAnalysisResponse, status_code=status.HTTP_200_OK)
async def analyze_ticket(request: TicketAnalysisRequest):
    """
    Analyzes digital support ticket, cross-references transaction logs,
    and applies safety filters. Bypasses LLM if prompt injection is detected.
    """
    logger.info(f"Received ticket analysis request: {request.ticket_id}")
    
    # 1. Pre-filtering: Prompt Injection Defense (RULE 4)
    if safety.detect_prompt_injection(request.complaint):
        logger.warning(f"Prompt injection detected on ticket {request.ticket_id}")
        raw_response = safety.generate_injection_response(request.ticket_id)
    else:
        # 2. Main LLM Analysis Loop (with built-in retries)
        raw_response = await analyzer.analyze_ticket_with_claude(request)
        
    # 3. Post-processing Sanitization (RULE 1, 2, 3, and Programmatic Routing Rules)
    sanitized_response = safety.post_process_sanitize(raw_response)
    
    # 4. Outgoing validation matching TicketAnalysisResponse schema
    try:
        validated_response = TicketAnalysisResponse(**sanitized_response)
        return validated_response
    except ValidationError as e:
        logger.error(f"Post-sanitization validation failed for ticket {request.ticket_id}: {str(e)}")
        # In case the post-processed result is somehow invalid, generate a standard fallback
        fallback = analyzer.generate_fallback_response(request, "Post-sanitization validation failure")
        return TicketAnalysisResponse(**fallback)
