from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import uuid
from .models import KnowledgeGroup, Document, KBJob

class CreateKnowledgeGroupView(APIView):
    def post(self, request):
        name = request.data.get('knowledgeGroupName')
        if not name:
            return Response({"status": "Failed", "exeption": "Name required"}, status=status.HTTP_400_BAD_REQUEST)
        
        kg_id = f"KG{str(uuid.uuid4().int)[:3]}"
        group = KnowledgeGroup.objects.create(id=kg_id, name=name)
        
        return Response({
            "status": "Success",
            "knowledgeGroupId": group.id,
            "knowledgeGroupName": group.name,
            "exeption": None
        }, status=status.HTTP_201_CREATED)

class GetKnowledgeGroupView(APIView):
    def get(self, request):
        groups = KnowledgeGroup.objects.all()
        results = [{"knowledgeGroupId": g.id, "knowledgeGroupName": g.name} for g in groups]
        return Response({
            "status": "Success",
            "results": results,
            "exeption": None
        }, status=status.HTTP_200_OK)

class GetKnowledgeGroupDetailsView(APIView):
    def get(self, request):
        groups = KnowledgeGroup.objects.all()
        results = []
        for g in groups:
            docs = [{"fileName": d.file_name, "docId": d.doc_id} for d in g.documents.all()]
            results.append({
                "knowledgeGroupId": g.id,
                "knowledgeGroupName": g.name,
                "documets": docs if docs else None
            })
        return Response({
            "status": "Success",
            "results": results,
            "exeption": None
        }, status=status.HTTP_200_OK)

class DocSubmitView(APIView):
    def post(self, request):
        data = request.data
        if not isinstance(data, list):
            return Response({"exeption": "Expected a list"}, status=status.HTTP_400_BAD_REQUEST)
        
        results = []
        exeptions = []
        
        for item in data:
            file_name = item.get('fileName')
            kg_id = item.get('knowledgeGroupId')
            
            try:
                # To simulate exceptions for missing group
                if kg_id:
                    kg = KnowledgeGroup.objects.get(id=kg_id)
                else:
                    kg = None
                    
                doc = Document.objects.create(
                    doc_id=f"doc{str(uuid.uuid4().int)[:6]}",
                    file_name=file_name,
                    knowledge_group=kg
                )
                results.append({
                    "fileName": doc.file_name,
                    "docId": doc.doc_id
                })
            except Exception as e:
                exeptions.append({
                    "fileName": file_name,
                    "exeption": str(e)
                })
                
        return Response({
            "status": "Success",
            "results": results,
            "exeptions": exeptions
        }, status=status.HTTP_200_OK)

class DocSubmitStatusView(APIView):
    def post(self, request):
        doc_id = request.data.get('docId')
        try:
            doc = Document.objects.get(doc_id=doc_id)
            return Response({
                "docId": doc.doc_id,
                "status": doc.status,
                "actualDocLink": doc.actual_url,
                "aiGeneratedDocLink": doc.ai_generated_url
            }, status=status.HTTP_200_OK)
        except Document.DoesNotExist:
            return Response({"exeption": "Not found"}, status=status.HTTP_404_NOT_FOUND)

class KBSubmitView(APIView):
    def post(self, request):
        links_str = request.data.get('links', '')
        if not links_str:
            return Response({"exeption": "Links required"}, status=status.HTTP_400_BAD_REQUEST)
            
        links = [l.strip() for l in links_str.split(';') if l.strip()]
        kb_ids = []
        for link in links:
            job = KBJob.objects.create(
                id=f"kbId{str(uuid.uuid4().int)[:4]}",
                url=link
            )
            kb_ids.append(job.id)
            
        return Response({
            "kbIds": "; ".join(kb_ids)
        }, status=status.HTTP_200_OK)

class KBSubmitStatusView(APIView):
    def post(self, request):
        kb_id = request.data.get('kbId')
        try:
            job = KBJob.objects.get(id=kb_id)
            return Response({
                "kbId": job.id,
                "status": job.status
            }, status=status.HTTP_200_OK)
        except KBJob.DoesNotExist:
            return Response({"exeption": "Not found"}, status=status.HTTP_404_NOT_FOUND)
