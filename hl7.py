# from hl7 message to database storage 

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dicom_dpacs.settings")
import django
django.setup()
from hl7apy.parser import parse_message
from hl7apy.exceptions import UnsupportedVersion
from django.views import View
from django.http import HttpResponse
import datetime
from datetime import date
from Modality.models import Order, Modality


def post():
    print('+++++++++')
    # try:
    hl7_file_path = os.path.join("media/hl7_messages", "hl7_message_1129757555111.100000025.hl7")
    with open(hl7_file_path, 'r') as hl7_file:
        hl7_message_str = hl7_file.read()
    # hl7_message_str = request.body.decode("utf-8")  # Get the HL7 message from the request
    hl7_message = hl7_message_str.split('\n')

    # Access the first PID segment
    pid_segment = hl7_message[4].split('|')

    # Accessing patient name (field index: 5)
    patient_name = pid_segment[5]

    # Accessing patient ID (field index: 3)
    patient_id = pid_segment[3]

    patient_sex = "M"
    patient_dob = date.today()
    referring_physicians_name = "DR.Bohra"
    requested_procedure_description = "Dummytestproc"
    study_instance_uid = "865ds3"
    station_id = "53792"
    modality_name = "CT"
    modality_description = "iugeih"
    modality_created_at = datetime.datetime.now()
    modality_updated_at = datetime.datetime.now()
    print("====================================")

    order = Order(
        patient_id=patient_id,
        patient_name=patient_name,
        patient_sex=patient_sex,
        patient_birth_date=patient_dob,
        referring_physicians_name=referring_physicians_name,
        requested_procedure_description=requested_procedure_description,
        study_instance_uid=study_instance_uid,
        station_id=station_id
    )
    order.save()

    modality = Modality(name=modality_name,description=modality_description, created_at=modality_created_at,updated_at=modality_updated_at)
    modality.save()

    return HttpResponse("HL7 data saved to the database.")

# obj1 = HL7ReceiverView()
post()
