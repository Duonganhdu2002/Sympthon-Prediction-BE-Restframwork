class Rule:
    def __init__(self, disease, symptoms):
        self.disease = disease
        self.symptoms = symptoms

class BackwardChaining:
    def __init__(self, rules):
        self.rules = rules

    def infer_disease(self, symptoms):
        inferred_diseases = []
        for rule in self.rules:
            if self._match(rule.symptoms, symptoms):
                inferred_diseases.append(rule.disease)
        return inferred_diseases

    def _match(self, rule_symptoms, patient_symptoms):
        return all(symptom in patient_symptoms for symptom in rule_symptoms)

    def get_related_diseases(self, symptoms):
        related_diseases = set()
        for rule in self.rules:
            if any(symptom in symptoms for symptom in rule.symptoms):
                related_diseases.add(rule.disease)
        return list(related_diseases)

    def get_disease_symptoms(self, disease_name):
        for rule in self.rules:
            if rule.disease == disease_name:
                return rule.symptoms
        return []

    def check_disease_with_symptoms(self, disease_name, patient_symptoms):
        for rule in self.rules:
            if rule.disease == disease_name:
                return self._match(rule.symptoms, patient_symptoms)
        return False
