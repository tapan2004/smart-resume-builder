from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from knowledge.models import Document, KnowledgeGroup
from django.db.models import Count, Q

class AdminDashboardView(APIView):
    def get(self, request):
        # We can implement dynamic aggregation, but to match the structure
        # provided in the example, we'll build a similar payload.
        
        # Calculate totals from the DB realistically
        all_docs = Document.objects.all()
        total_records = all_docs.count()
        
        statuses = ['submitted', 'Processing', 'Completed']
        results = []
        
        for st in statuses:
            st_docs = all_docs.filter(status=st)
            total_st = st_docs.count()
            
            # Group by knowledge group to simulate 'types'
            groups = KnowledgeGroup.objects.annotate(
                num_docs=Count('documents', filter=Q(documents__status=st))
            ).filter(num_docs__gt=0)
            
            types = []
            for g in groups:
                types.append({
                    "knowledgeGroupId": g.id,
                    "knowledgeGroupName": g.name,
                    "numberOfDocs": g.num_docs
                })
                
            results.append({
                "status": st,
                "totalNumberOfDocs": total_st,
                "types": types
            })
            
        return Response({
            "status": "Success",
            "totalNumberOfRecords": total_records,
            "results": results,
            "exeption": None
        }, status=status.HTTP_200_OK)
