# diagnosis/management/commands/load_rules.py
import csv
from django.core.management.base import BaseCommand
from diagnosis.models import Rule

class Command(BaseCommand):
    help = 'Load rules from a CSV file into the database'

    def handle(self, *args, **kwargs):
        with open('D:/AI/DiseaseDiagnosis/diagnosis/management/commands/dataset.csv', 'r') as file:  # Update the path to your CSV file
            reader = csv.reader(file)
            next(reader)  # Skip header row
            for row in reader:
                disease = row[0].lower().strip()
                symptoms = ','.join([symptom.strip().lower().replace(" ", "_") for symptom in row[1:] if symptom.strip()])
                Rule.objects.create(disease=disease, symptoms=symptoms)
        self.stdout.write(self.style.SUCCESS('Successfully loaded rules from CSV'))
