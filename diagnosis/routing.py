from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/diagnosis/', consumers.DiagnosisConsumer.as_asgi()),
]
