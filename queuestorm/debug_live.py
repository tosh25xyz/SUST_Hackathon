import os
import asyncio
import logging
from dotenv import load_dotenv

# Load env
load_dotenv()

logging.basicConfig(level=logging.INFO)

from models import TicketAnalysisRequest
from analyzer import analyze_ticket_with_openrouter

request = TicketAnalysisRequest(
    ticket_id="TEST-C1",
    complaint="I sent 5000 taka to the wrong number around 2pm today",
    language="en",
    transaction_history=[
        {
            "transaction_id": "TXN-TEST1",
            "timestamp": "2026-04-14T14:08:00Z",
            "type": "transfer",
            "amount": 5000,
            "counterparty": "+8801719876543",
            "status": "completed"
        }
    ]
)

async def main():
    print("Starting analyze_ticket_with_openrouter call...")
    try:
        res = await analyze_ticket_with_openrouter(request)
        print("Completed analyze_ticket_with_openrouter!")
        print("Result:")
        print(res)
    except Exception as e:
        print(f"Failed with exception: {e}")

asyncio.run(main())
