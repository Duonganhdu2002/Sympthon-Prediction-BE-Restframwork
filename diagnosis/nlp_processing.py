import spacy
from asgiref.sync import sync_to_async
from .models import Rule

# Tải mô hình ngôn ngữ tiếng Anh
nlp = spacy.load("en_core_web_sm")

@sync_to_async
def get_disease_and_symptom_list():
    """
    Hàm này đọc danh sách các bệnh và triệu chứng từ cơ sở dữ liệu và trả về một tập hợp các bệnh và triệu chứng.
    """
    diseases = set()
    symptoms = set()
    rules = Rule.objects.all()
    for rule in rules:
        disease = rule.disease.strip().lower().replace(" ", "_")
        diseases.add(disease)
        rule_symptoms = rule.symptoms.split(',')
        for symptom in rule_symptoms:
            symptom = symptom.strip().lower().replace(" ", "_")
            symptoms.add(symptom)
    return diseases, symptoms

async def extract_symptoms_and_diseases(text):
    """
    Hàm này nhận vào một chuỗi văn bản và trả về danh sách các triệu chứng và bệnh được phát hiện.
    """
    doc = nlp(text)
    symptoms = set()
    diseases = set()

    # Lấy danh sách bệnh và triệu chứng từ cơ sở dữ liệu
    common_diseases, common_symptoms = await get_disease_and_symptom_list()

    # Kiểm tra từng cụm danh từ (noun chunks) trong văn bản
    for chunk in doc.noun_chunks:
        term = chunk.text.lower().replace(" ", "_")
        if term in common_symptoms:
            symptoms.add(term)
        if term in common_diseases:
            diseases.add(term)

    # Kiểm tra từng token trong văn bản
    for token in doc:
        token_text = token.text.lower().replace(" ", "_")
        if token_text in common_symptoms:
            symptoms.add(token_text)
        if token_text in common_diseases:
            diseases.add(token_text)

    # Kiểm tra bigrams trong văn bản
    for i in range(len(doc) - 1):
        bigram = f"{doc[i].text.lower().replace(' ', '_')}_{doc[i+1].text.lower().replace(' ', '_')}"
        if bigram in common_symptoms:
            symptoms.add(bigram)
        if bigram in common_diseases:
            diseases.add(bigram)

    print("Triệu chứng:", list(symptoms))
    print("Bệnh:", list(diseases))
    return list(symptoms), list(diseases)
