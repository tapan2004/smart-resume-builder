from django.urls import path
from .views import (
    CreateKnowledgeGroupView,
    GetKnowledgeGroupView,
    GetKnowledgeGroupDetailsView,
    DocSubmitView,
    DocSubmitStatusView,
    KBSubmitView,
    KBSubmitStatusView
)

urlpatterns = [
    path('group/create/', CreateKnowledgeGroupView.as_view(), name='create-group'),
    path('group/list/', GetKnowledgeGroupView.as_view(), name='list-group'),
    path('group/details/', GetKnowledgeGroupDetailsView.as_view(), name='details-group'),
    path('doc/submit/', DocSubmitView.as_view(), name='doc-submit'),
    path('doc/status/', DocSubmitStatusView.as_view(), name='doc-status'),
    path('kb/submit/', KBSubmitView.as_view(), name='kb-submit'),
    path('kb/status/', KBSubmitStatusView.as_view(), name='kb-status'),
]
