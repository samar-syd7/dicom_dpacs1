import hl7apy.parser
import os
from pydicom import dcmwrite
from pydicom.dataset import Dataset

print("Started....conversion")
hl7_file_path = 'media/hl7_messages/hl7_message_1129757555111.100000025.hl7'
with open(hl7_file_path, 'r') as hl7_file:
    hl7_message_str = hl7_file.read()

# Parse the HL7 message
hl7_message = hl7apy.parse_message(hl7_message_str)

# Extract relevant information from the HL7 message
patient_name = hl7_message.PID[5][0][0]
patient_id = hl7_message.PID[3][0][0]

# Create a Modality Worklist DICOM dataset
dicom_dataset = Dataset()
dicom_dataset.PatientName = patient_name
dicom_dataset.PatientID = patient_id
dicom_dataset.ScheduledProcedureStepDescription = "CT Abdomen"
dicom_dataset.ScheduledProcedureStepID = "SPS123"

output_path = "media/modality_worklist/"

# Save the DICOM dataset as a .dcm file
output_filename = os.path.join(output_path, f"{patient_name.replace('^', '_')}.dcm")
dcmwrite(output_filename, dicom_dataset)

print(f"DICOM dataset saved as {output_filename}")
