from rest_framework import generics
from .models import Rule, UserFeedback
from .serializers import RuleSerializer, UserFeedbackSerializer

class RuleListCreateView(generics.ListCreateAPIView):
    queryset = Rule.objects.all()
    serializer_class = RuleSerializer

class UserFeedbackListCreateView(generics.ListCreateAPIView):
    queryset = UserFeedback.objects.all()
    serializer_class = UserFeedbackSerializer
