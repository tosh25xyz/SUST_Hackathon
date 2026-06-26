import json
import httpx

def run_tests():
    url = "http://localhost:8000/analyze-ticket"
    
    tests = [
        {
            "name": "TEST 1 — CONSISTENT",
            "input": {
                "ticket_id": "TEST-C1",
                "complaint": "I sent 5000 taka to the wrong number around 2pm today",
                "language": "en",
                "transaction_history": [
                    {
                        "transaction_id": "TXN-TEST1",
                        "timestamp": "2026-04-14T14:08:00Z",
                        "type": "transfer",
                        "amount": 5000,
                        "counterparty": "+8801719876543",
                        "status": "completed"
                    }
                ]
            },
            "expected": {
                "evidence_verdict": "consistent",
                "case_type": "wrong_transfer"
            }
        },
        {
            "name": "TEST 2 — INCONSISTENT",
            "input": {
                "ticket_id": "TEST-C2",
                "complaint": "my payment failed but money was deducted",
                "language": "en",
                "transaction_history": [
                    {
                        "transaction_id": "TXN-TEST2",
                        "timestamp": "2026-04-14T10:00:00Z",
                        "type": "payment",
                        "amount": 1000,
                        "counterparty": "BILLER-DESCO",
                        "status": "completed"
                    }
                ]
            },
            "expected": {
                "evidence_verdict": "inconsistent",
                "case_type": "payment_failed"
            }
        },
        {
            "name": "TEST 3 — INSUFFICIENT DATA",
            "input": {
                "ticket_id": "TEST-C3",
                "complaint": "I sent 1000 to my brother yesterday but he says he did not get it",
                "language": "en",
                "transaction_history": [
                    {
                        "transaction_id": "TXN-TEST3A",
                        "timestamp": "2026-04-13T11:00:00Z",
                        "type": "transfer",
                        "amount": 1000,
                        "counterparty": "+8801712001122",
                        "status": "completed"
                    },
                    {
                        "transaction_id": "TXN-TEST3B",
                        "timestamp": "2026-04-13T19:00:00Z",
                        "type": "transfer",
                        "amount": 1000,
                        "counterparty": "+8801812334455",
                        "status": "completed"
                    }
                ]
            },
            "expected": {
                "evidence_verdict": "insufficient_data",
                "relevant_transaction_id": None
            }
        }
    ]
    
    print("=" * 60)
    print("Running Evidence Tests against localhost:8000...")
    print("=" * 60)
    
    all_passed = True
    for test in tests:
        name = test["name"]
        payload = test["input"]
        expected = test["expected"]
        
        print(f"\nRunning {name}...")
        
        try:
            response = httpx.post(url, json=payload, timeout=120.0)
            if response.status_code != 200:
                print(f"  [FAIL] HTTP status: {response.status_code}")
                all_passed = False
                continue
                
            actual = response.json()
            test_passed = True
            
            for field, expected_val in expected.items():
                actual_val = actual.get(field)
                if actual_val == expected_val:
                    print(f"  - {field}: PASS (Value: {actual_val})")
                else:
                    print(f"  - {field}: FAIL (Expected: {expected_val}, Actual: {actual_val})")
                    test_passed = False
                    
            if test_passed:
                print(f"Result: {name} PASSED")
            else:
                print(f"Result: {name} FAILED")
                all_passed = False
                
        except Exception as e:
            print(f"  [ERROR] {e}")
            all_passed = False
            
    print("=" * 60)
    if all_passed:
        print("ALL EVIDENCE TESTS PASSED!")
    else:
        print("SOME EVIDENCE TESTS FAILED.")
    print("=" * 60)

if __name__ == "__main__":
    run_tests()
