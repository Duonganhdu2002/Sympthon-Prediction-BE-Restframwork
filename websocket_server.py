import asyncio
import websockets
import os
import django
import json
from asgiref.sync import sync_to_async
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DiseaseDiagnosis.settings')
django.setup()

from diagnosis.models import Rule, UserFeedback
from diagnosis.backward_chaining import BackwardChaining, Rule as BCRule
from diagnosis.nlp_processing import extract_symptoms_and_diseases

@sync_to_async
def get_rules():
    return [BCRule(rule.disease, rule.symptoms.split(',')) for rule in Rule.objects.all()]

@sync_to_async
def save_user_feedback(user_message, detected_symptoms, inferred_disease, correct_diagnosis="", feedback=""):
    UserFeedback.objects.create(
        user_message=user_message,
        detected_symptoms=detected_symptoms,
        inferred_disease=inferred_disease,
        correct_diagnosis=correct_diagnosis,
        feedback=feedback,
    )

async def process_message(message):
    try:
        data = json.loads(message)
        text = data.get('message', '')

        if not text:
            return json.dumps({"message": "Hi, I'm Layla, your virtual nurse. It seems like you didn't provide any symptoms. Could you please describe what you're experiencing?"})

        rules = await get_rules()
        backward_chaining = BackwardChaining(rules)
        response_message = await backward_chaining.handle_input(text)

        symptoms, diseases = await extract_symptoms_and_diseases(text)
        await save_user_feedback(text, ", ".join(symptoms), ", ".join(diseases))
        return json.dumps({'message': response_message})
    except Exception as e:
        return json.dumps({"error": str(e)})

async def echo(websocket, path):
    async for message in websocket:
        response = await process_message(message)
        await websocket.send(response)

start_server = websockets.serve(echo, "localhost", 8000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
