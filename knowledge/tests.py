from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
import json

class APITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.create_group_url = reverse('create-group')
        self.doc_submit_url = reverse('doc-submit')
        self.doc_status_url = reverse('doc-status')
        self.kb_submit_url = reverse('kb-submit')
        self.kb_status_url = reverse('kb-status')
        self.dashboard_url = reverse('admin-dashboard')

    def test_complete_flow(self):
        # 1. Create Knowledge Group
        kg_response = self.client.post(self.create_group_url, {"knowledgeGroupName": "Security Rule Document"}, format='json')
        self.assertEqual(kg_response.status_code, status.HTTP_201_CREATED)
        kg_id = kg_response.data['knowledgeGroupId']
        self.assertIsNotNone(kg_id)
        print("\n[OK] Knowledge Group Created:", kg_response.data)

        # 2. Submit Documents
        doc_payload = [
            {"fileName": "example1.pdf", "knowledgeGroupId": kg_id},
            {"fileName": "example2.pdf", "knowledgeGroupId": kg_id}
        ]
        doc_res = self.client.post(self.doc_submit_url, doc_payload, format='json')
        self.assertEqual(doc_res.status_code, status.HTTP_200_OK)
        # Verify both docs got their IDs
        doc_results = doc_res.data['results']
        self.assertEqual(len(doc_results), 2)
        doc1_id = doc_results[0]['docId']
        print("[OK] Documents Submitted:", doc_res.data)

        # 3. Check Document Status
        status_res = self.client.post(self.doc_status_url, {"docId": doc1_id}, format='json')
        self.assertEqual(status_res.status_code, status.HTTP_200_OK)
        self.assertEqual(status_res.data['status'], 'submitted')
        print("[OK] Document Status Checked:", status_res.data)

        # 4. Submit KB Links
        kb_payload = {"links": "https://example.com/link1.html; https://example.com/link2.html"}
        kb_res = self.client.post(self.kb_submit_url, kb_payload, format='json')
        self.assertEqual(kb_res.status_code, status.HTTP_200_OK)
        kb_ids = kb_res.data['kbIds'].split('; ')
        self.assertEqual(len(kb_ids), 2)
        print("[OK] KB Links Submitted:", kb_res.data)

        # 5. Check KB Status
        kb1_id = kb_ids[0]
        kb_status_res = self.client.post(self.kb_status_url, {"kbId": kb1_id}, format='json')
        self.assertEqual(kb_status_res.status_code, status.HTTP_200_OK)
        self.assertEqual(kb_status_res.data['status'], 'Submitted')
        print("[OK] KB Status Checked:", kb_status_res.data)

        # 6. Check Admin Dashboard
        dashboard_res = self.client.get(self.dashboard_url)
        self.assertEqual(dashboard_res.status_code, status.HTTP_200_OK)
        dashboard_data = dashboard_res.data
        self.assertEqual(dashboard_data['status'], 'Success')
        # Total docs should be 2 right now
        print("[OK] Admin Dashboard Loaded:", json.dumps(dashboard_data, indent=2))
