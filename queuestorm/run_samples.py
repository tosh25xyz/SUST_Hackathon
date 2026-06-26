import json
import httpx
import os

def run():
    url = "http://localhost:8000/analyze-ticket"
    cases_file = "SUST_Preli_Sample_Cases.json"
    
    if not os.path.exists(cases_file):
        print(f"Error: {cases_file} not found in current directory.")
        return
        
    with open(cases_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    cases = data.get("cases", [])
    total_cases = len(cases)
    fully_matched = 0
    
    sample_01_response = None
    
    fields_to_compare = [
        "ticket_id",
        "relevant_transaction_id",
        "evidence_verdict",
        "case_type",
        "department",
        "human_review_required"
    ]
    
    print("=" * 60)
    print("Running Sample Cases validation against localhost:8000...")
    print("=" * 60)
    
    for case in cases:
        case_id = case.get("id")
        case_input = case.get("input")
        expected_output = case.get("expected_output")
        
        print(f"\nAnalyzing Case: {case_id} - {case.get('label')}")
        
        try:
            response = httpx.post(url, json=case_input, timeout=120.0)
            if response.status_code != 200:
                print(f"  [ERROR] Received status code {response.status_code}")
                continue
                
            actual_output = response.json()
            
            if case_id == "SAMPLE-01":
                sample_01_response = actual_output
                
            # Compare fields
            case_passed = True
            for field in fields_to_compare:
                actual_val = actual_output.get(field)
                expected_val = expected_output.get(field)
                
                if actual_val == expected_val:
                    print(f"  - {field:25}: PASS (Value: {actual_val})")
                else:
                    print(f"  - {field:25}: FAIL (Expected: {expected_val}, Actual: {actual_val})")
                    case_passed = False
                    
            if case_passed:
                fully_matched += 1
                print(f"Result: {case_id} PASSED")
            else:
                print(f"Result: {case_id} FAILED")
                
        except Exception as e:
            print(f"  [ERROR] Request failed: {e}")
            
    # Save SAMPLE-01 response
    if sample_01_response:
        output_file = "sample_output.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(sample_01_response, f, indent=2, ensure_ascii=False)
        print(f"\n[INFO] Saved SAMPLE-01 full response to {output_file}")
        
    print("=" * 60)
    print(f"Total score: {fully_matched}/{total_cases} cases fully matched")
    print("=" * 60)

if __name__ == "__main__":
    run()
