import os
from hl7apy.parser import parse_message
from hl7apy.exceptions import UnsupportedVersion
from django.views import View
from django.http import JsonResponse
# from Modality.models import Order

class HL7ReceiverView(View):
    def post(self, request, *args, **kwargs):
        hl7_message_str = request.body.decode("utf-8")  # Get the HL7 message from the request
        
        try:
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
            
            Order.objects.create(
                patient_id=patient_id,
                patient_name=patient_name,
                patient_sex=patient_sex,
                patient_dob=patient_dob,
                referring_physicians_name=referring_physicians_name

            )
            
            return JsonResponse({"message": "HL7 data saved to the database."})
        
        except UnsupportedVersion:
            return JsonResponse({"error": "Unsupported HL7 version."})
        except Exception as e:
            return JsonResponse({"error": f"An error occurred: {e}"})
