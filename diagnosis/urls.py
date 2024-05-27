from django.urls import path
from .views import RuleListCreateView, UserFeedbackListCreateView

urlpatterns = [
    path('rules/', RuleListCreateView.as_view(), name='rule-list-create'),
    path('feedback/', UserFeedbackListCreateView.as_view(), name='user-feedback-list-create'),
]
