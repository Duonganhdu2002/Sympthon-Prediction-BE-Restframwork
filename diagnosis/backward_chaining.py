class Rule:
    def __init__(self, disease, symptoms):
        self.disease = disease
        self.symptoms = symptoms

class BackwardChaining:
    def __init__(self, rules):
        self.rules = rules

    def infer_disease(self, symptoms):
        possible_diseases = set()
        for rule in self.rules:
            if all(symptom in symptoms for symptom in rule.symptoms):
                possible_diseases.add(rule.disease)
        return list(possible_diseases)

    def get_related_diseases(self, symptoms):
        related_diseases = set()
        for rule in self.rules:
            if any(symptom in rule.symptoms for symptom in symptoms):
                related_diseases.add(rule.disease)
        return list(related_diseases)
