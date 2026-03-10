from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Recommendation
from .serializers import RecommendationSerializer
import random

class RecommendationList(APIView):
    def get(self, request, customer_id):
        recs = Recommendation.objects.filter(customer_id=customer_id)
        if not recs.exists():
            # Mock some AI logic: return random recommendations
            return Response([
                {"recommended_book_id": random.randint(1, 100), "score": 0.95},
                {"recommended_book_id": random.randint(1, 100), "score": 0.88}
            ])
        serializer = RecommendationSerializer(recs, many=True)
        return Response(serializer.data)
