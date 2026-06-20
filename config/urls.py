from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/accounts/', include('accounts.urls')),
    path('api/v1/knowledge/', include('knowledge.urls')),
    path('api/v1/dashboard/', include('dashboard.urls')),
]
