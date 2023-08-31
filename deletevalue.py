import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dicom_dpacs.settings")
import django
django.setup()

# Now you can import the models and perform database operations
from Modality.models import Study, Series, Image, Patient

# Delete all data from the Image table
Image.objects.all().delete()

# Delete all data from the Series table
Series.objects.all().delete()

# Delete all data from the Study table
Study.objects.all().delete()

Patient.objects.all().delete()
