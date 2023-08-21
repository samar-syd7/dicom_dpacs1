import hl7
from hl7.exceptions import ParseException

message_path = 'media/hl7_messages/hl7_message_101109.hl7'
try:
    with open(message_path, 'r') as message_file:
        hl7_message_str = message_file.read()

    hl7_message = hl7.parse(hl7_message_str)

    # Access the PID segment (index 1) in the HL7 message
    pid_segment = hl7_message[1]

    # Access the patient's name (PID-5) and ID (PID-3)
    patient_name = pid_segment[5][0][0]
    patient_id = pid_segment[3][0][0]

    print("Patient Name:", patient_name)
    print("Patient ID:", patient_id)

except ParseException as parse_exception:
    print("Parse Exception:", parse_exception)
except Exception as ex:
    print("An error occurred:", ex)
