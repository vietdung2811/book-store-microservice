from django.urls import path
from app.views import RecommendationList

urlpatterns = [
    path('recommendations/<int:customer_id>/', RecommendationList.as_view()),
]
