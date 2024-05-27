import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import Rule
from .backward_chaining import BackwardChaining, Rule as BCRule
from .nlp_processing import extract_symptoms

class DiagnosisConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        text = data.get('message', '')

        if not text:
            await self.send(text_data=json.dumps({"error": "No message provided"}))
            return

        symptoms = extract_symptoms(text)
        if not symptoms:
            await self.send(text_data=json.dumps({"error": "No symptoms detected in the message"}))
            return

        rules = await sync_to_async(list)(Rule.objects.all())
        rules = [BCRule(rule.disease, rule.symptoms.split(',')) for rule in rules]
        backward_chaining = BackwardChaining(rules)
        inferred_diseases = backward_chaining.infer_disease(symptoms)

        if inferred_diseases:
            await self.send(text_data=json.dumps({'disease': inferred_diseases[0]}))
        else:
            related_diseases = backward_chaining.get_related_diseases(symptoms)
            if related_diseases:
                await self.send(text_data=json.dumps({'diseases': ', '.join(related_diseases)}))
            else:
                await self.send(text_data=json.dumps({'message': 'No diseases found.'}))
