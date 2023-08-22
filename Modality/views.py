from django.shortcuts import render,HttpResponse
from .models import Order,Modality
import datetime
# Create your views here.
def home(request):
    data = Order(
        patient_name="Amer",
        patient_id="54462",
        patient_sex = "M",
        patient_birth_date = datetime.datetime.now(),
        referring_physicians_name = "DR.Bohra",
        requested_procedure_description = "Dummytestproc",
        study_instance_uid = "865ds3",
        station_id = "53792",
        created_at = datetime.datetime.now(),
        updated_at = datetime.datetime.now()

    )
    data.save()

    data2 = Modality(
         name="CT",
         description="uoert8",
         created_at = datetime.datetime.now(),
         updated_at = datetime.datetime.now()
    )
    data2.save()
    return HttpResponse("Data Created")

import os
def post(request):
    print('---------')
    # try:
    hl7_file_path = os.path.join("media/hl7_messages","hl7_message_101109.hl7")
    with open(hl7_file_path, 'r') as hl7_file:
        hl7_message_str=hl7_file.read()
    #hl7_message_str = request.body.decode("utf-8")  # Get the HL7 message from the request
    hl7_message = hl7_message_str.split('\n')
    
    # Access the first PID segment
    pid_segment = hl7_message[1].split('|')
    
    # Accessing patient name (field index: 5)
    patient_name = pid_segment[5]
    
    # Accessing patient ID (field index: 3)
    patient_id = pid_segment[3]
    
    patient_sex = "M"
    patient_dob = "12042006"
    referring_physicians_name = "DR.Bohra"
    requested_procedure_description = "Dummytestproc"
    study_instance_uid = "865ds3"
    station_id = "53792"
    modality_name = "CT"
    modality_description="iugeih"
    modality_created_at=datetime.datetime.now()
    modality_updated_at=datetime.datetime.now()
    print("====================================")

    order = Order(
        patient_id=patient_id,
        patient_name=patient_name,
        patient_sex=patient_sex,
        patient_birth_date=datetime.datetime.now(),
        referring_physicians_name=referring_physicians_name,
        requested_procedure_description=requested_procedure_description,
        study_instance_uid=study_instance_uid,
        station_id=station_id


    ).save()

    modality = Modality(description= modality_description,created_at= datetime.datetime.now(),name="Sample Name")
    modality.save()

    return HttpResponse("HL7 data saved to the database.")
    
    # except :
    #     return HttpResponse({"error": "Unsupported HL7 version."})
    # except Exception as e:
    #     return HttpResponse({"error": f"An error occurred: {e}"})
