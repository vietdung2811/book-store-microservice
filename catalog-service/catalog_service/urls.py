from django.urls import path
from app.views import CategoryListCreate, CatalogOverview

urlpatterns = [
    path('categories/', CategoryListCreate.as_view()),
    path('overview/', CatalogOverview.as_view()),
]
