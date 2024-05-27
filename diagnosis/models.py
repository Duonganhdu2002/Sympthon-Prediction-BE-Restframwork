from django.db import models

class Rule(models.Model):
    disease = models.CharField(max_length=255)
    symptoms = models.TextField()

class UserFeedback(models.Model):
    user_message = models.TextField()
    detected_symptoms = models.TextField()
    inferred_disease = models.TextField()
    correct_diagnosis = models.TextField(blank=True, null=True)
    feedback = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
