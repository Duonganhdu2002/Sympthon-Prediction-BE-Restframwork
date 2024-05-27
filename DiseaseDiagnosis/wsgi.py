import os
from django.core.wsgi import get_wsgi_application

# Thiết lập biến môi trường DJANGO_SETTINGS_MODULE
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DiseaseDiagnosis.settings')

application = get_wsgi_application()
