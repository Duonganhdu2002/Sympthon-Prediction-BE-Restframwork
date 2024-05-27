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
from diagnosis.nlp_processing import extract_symptoms

async def get_rules():
    return [BCRule(rule.disease, rule.symptoms.split(',')) for rule in await sync_to_async(list)(Rule.objects.all())]

def create_response_message(disease, related_diseases):
    if disease:
        return f"Hello, I'm Layla, your virtual nurse. Based on the symptoms you provided, it seems like you might be experiencing symptoms of {disease}. I recommend that you consult with a healthcare professional for a proper diagnosis and treatment. Remember, taking care of your health is important. Feel better soon!"
    elif related_diseases:
        return f"Hi there, I'm Layla. From what you've described, it seems like you might be experiencing something related to: {', '.join(related_diseases)}. It's always best to check with a healthcare provider to get a precise diagnosis. Stay safe and take care!"
    else:
        return "Hi, I'm Layla, your virtual nurse. I'm sorry, but I couldn't find a match for your symptoms. It might be a good idea to see a healthcare professional for an accurate diagnosis. Please take care of yourself!"

async def save_user_feedback(user_message, detected_symptoms, inferred_disease, correct_diagnosis="", feedback=""):
    await sync_to_async(UserFeedback.objects.create)(
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

        symptoms = extract_symptoms(text)
        if not symptoms:
            return json.dumps({"message": "Hi, I'm Layla. I couldn't detect any symptoms in your message. Could you please describe your symptoms in more detail?"})

        rules = await get_rules()
        backward_chaining = BackwardChaining(rules)
        inferred_diseases = backward_chaining.infer_disease(symptoms)

        response_message = ""
        if inferred_diseases:
            response_message = create_response_message(inferred_diseases[0], None)
            await save_user_feedback(text, ", ".join(symptoms), inferred_diseases[0])
        else:
            related_diseases = backward_chaining.get_related_diseases(symptoms)
            response_message = create_response_message(None, related_diseases)
            await save_user_feedback(text, ", ".join(symptoms), "None", ", ".join(related_diseases))

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