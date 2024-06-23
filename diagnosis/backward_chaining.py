from collections import defaultdict
from diagnosis.nlp_processing import extract_symptoms_and_diseases

class Rule:
    def __init__(self, disease, symptoms):
        self.disease = disease
        self.symptoms = symptoms

class BackwardChaining:
    def __init__(self, rules):
        self.rules = defaultdict(set)  # Use set to avoid duplicate symptoms
        self.facts = set()
        for rule in rules:
            disease = rule.disease.lower().strip()
            self.rules[disease].update([symptom.lower().strip() for symptom in rule.symptoms])

    def add_fact(self, fact):
        self.facts.add(fact.lower().strip())

    def backward_chain(self, goal):
        if goal in self.facts:
            return True
        for symptom in self.rules.get(goal, []):
            if self.backward_chain(symptom):
                return True
        return False

    def get_related_diseases(self, symptoms):
        related_diseases = []
        for disease, disease_symptoms in self.rules.items():
            if any(symptom in symptoms for symptom in disease_symptoms):
                related_diseases.append(disease)
        return related_diseases

    def check_disease_with_symptoms(self, disease, symptoms):
        required_symptoms = self.rules.get(disease, [])
        return all(symptom in symptoms for symptom in required_symptoms)

    def get_disease_symptoms(self, disease):
        disease = disease.lower().strip()
        return list(self.rules.get(disease, []))  # Convert set back to list

    def create_response_message(self, disease=None, related_diseases=None):
        if disease:
            return f"It seems like you might be experiencing symptoms of {disease}."
        elif related_diseases:
            return f"It seems like you might be experiencing something related to: {', '.join(related_diseases)}"
        else:
            return "I'm sorry, but I couldn't find a match for your symptoms."

    async def handle_input(self, text):
        symptoms, diseases = await extract_symptoms_and_diseases(text)
        response_message = ""

        # Normalize symptoms and diseases
        symptoms = [symptom.lower().strip() for symptom in symptoms]
        diseases = [disease.lower().strip() for disease in diseases]

        if diseases and not symptoms:
            # Case 1: User provided only a disease name
            disease_name = diseases[0]
            disease_symptoms = self.get_disease_symptoms(disease_name)
            if disease_symptoms:
                response_message = f"The symptoms of {disease_name} are: {', '.join(disease_symptoms)}. Do you have these symptoms?"
            else:
                response_message = f"The symptoms of {disease_name} are not available. Do you have these symptoms?"

        elif symptoms and not diseases:
            # Case 2: User provided only symptoms
            inferred_diseases = self.get_related_diseases(symptoms)
            if inferred_diseases:
                response_message = self.create_response_message(disease=inferred_diseases[0])
            else:
                response_message = self.create_response_message(related_diseases=self.get_related_diseases(symptoms))

        elif diseases and symptoms:
            # Case 3: User provided both disease name and symptoms
            disease_name = diseases[0]
            if self.check_disease_with_symptoms(disease_name, symptoms):
                response_message = f"Based on the symptoms you provided, it seems like you might be experiencing symptoms of {disease_name}."
            else:
                disease_symptoms = self.get_disease_symptoms(disease_name)
                related_diseases = self.get_related_diseases(symptoms)
                related_diseases = [d for d in related_diseases if d != disease_name]
                response_message = f"The symptoms you provided do not match completely with {disease_name}. However, the symptoms of {disease_name} are: {', '.join(disease_symptoms)}. You might also be experiencing something related to: {', '.join(related_diseases)}."

        return response_message
