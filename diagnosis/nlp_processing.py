import spacy

# Tải mô hình ngôn ngữ tiếng Anh
nlp = spacy.load("en_core_web_sm")

def extract_symptoms(text):
    """
    Hàm này nhận vào một chuỗi văn bản và trả về danh sách các triệu chứng được phát hiện.
    """
    doc = nlp(text)
    symptoms = []

    # Giả định rằng các triệu chứng là các danh từ hoặc danh từ ghép
    for chunk in doc.noun_chunks:
        symptom = chunk.text.lower().replace(" ", "_")
        symptoms.append(symptom)

    return symptoms
