import requests
import json
import time
import os
import subprocess

BASE_URL = "http://127.0.0.1:8000/api/v1"

def print_section(title):
    print(f"\n{'='*50}\n{title}\n{'='*50}")

def test_apis():
    # 1. Create Knowledge Group
    print_section("1. Testing Create Knowledge Group API (POST)")
    kg_payload = {"knowledgeGroupName": "Security Rule Document"}
    res = requests.post(f"{BASE_URL}/knowledge/group/create/", json=kg_payload)
    print("Response payload:", json.dumps(res.json(), indent=2))
    
    kg_id = res.json().get('knowledgeGroupId')
    if not kg_id:
        print("Failed to get Knowledge Group ID. Exiting.")
        return

    # 2. Document Submission
    print_section("2. Testing Document Submit API (POST)")
    doc_payload = [
        {"fileName": "example1.pdf", "knowledgeGroupId": kg_id},
        {"fileName": "example2.pdf", "knowledgeGroupId": kg_id}
    ]
    res = requests.post(f"{BASE_URL}/knowledge/doc/submit/", json=doc_payload)
    print("Response payload:", json.dumps(res.json(), indent=2))
    
    docs = res.json().get('results', [])
    doc_id = docs[0]['docId'] if docs else None
    
    # 3. Document Submission Status
    if doc_id:
        print_section("3. Testing Document Status API (POST)")
        status_payload = {"docId": doc_id}
        res = requests.post(f"{BASE_URL}/knowledge/doc/status/", json=status_payload)
        print("Response payload:", json.dumps(res.json(), indent=2))

    # 4. KB Submit
    print_section("4. Testing KB Submit API (POST)")
    kb_payload = {"links": "https://example.com/link1.html; https://example.com/link2.html"}
    res = requests.post(f"{BASE_URL}/knowledge/kb/submit/", json=kb_payload)
    print("Response payload:", json.dumps(res.json(), indent=2))
    
    kb_ids_str = res.json().get('kbIds')
    if kb_ids_str:
        kb_id = kb_ids_str.split('; ')[0]
        # 5. KB Submit Status
        print_section("5. Testing KB Status API (POST)")
        kb_stat_payload = {"kbId": kb_id}
        res = requests.post(f"{BASE_URL}/knowledge/kb/status/", json=kb_stat_payload)
        print("Response payload:", json.dumps(res.json(), indent=2))

    # 6. Admin Dashboard
    print_section("6. Testing Admin Dashboard API (GET)")
    res = requests.get(f"{BASE_URL}/dashboard/dashboard/")
    print("Response payload:", json.dumps(res.json(), indent=2))

if __name__ == "__main__":
    print("Please make sure your Django server is running via:")
    print("> python manage.py runserver 8000")
    print("Wait 3 seconds before executing...")
    time.sleep(3)
    try:
        test_apis()
    except requests.exceptions.ConnectionError:
        print("\n[ERROR] Connection failed. Please start your Django server first.")
