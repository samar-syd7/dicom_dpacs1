import os
from pydicom import dcmwrite
from pydicom.dataset import Dataset
# from hl7 import parse
from hl7apy.parser import parse_message
from hl7apy.exceptions import UnsupportedVersion

print("Started....conversion")
hl7_file_path = 'media/hl7_messages/hl7_message_101109.hl7'
    # print(hl7_message_str, "------")
    # print("\n")

try:

    with open(hl7_file_path, 'r') as hl7_file:
        hl7_message_str = hl7_file.read()
    hl7_message = hl7_message_str.split('\n')
    #hl7_message2 = parse_message(message)

    #print(type(hl7_message2))
    #print(hl7_message2._get_children('SEG')[1])
    # print(xcvxf)

    # Access the first PID segment
    pid_segment = hl7_message[1].split('|')

    # Accessing patient name (field index: 5)
    patient_name = pid_segment[5]

    # Accessing patient ID (field index: 3)
    patient_id = pid_segment[3]

    # Create a Modality Worklist DICOM dataset
    dicom_dataset = Dataset()
    dicom_dataset.PatientName = "Amer"
    dicom_dataset.PatientID = patient_id
    dicom_dataset.AccessionNumber = "673986"
    dicom_dataset.Modality = "CT"
    dicom_dataset.RequestedProcID = "SPS123"
    dicom_dataset.ScheduledProcStepStartDate = "04092014"
    dicom_dataset.ScheduledStationAETitle = "CT_MOD"

    print(dicom_dataset,'\n\n','---------')

    dicom_dataset.is_little_endian=True
    dicom_dataset.is_implicit_VR=True


    output_path = "media/modality_worklist/"

    # Saving the DICOM dataset as a .dcm file
    output_filename = os.path.join(output_path, f"{patient_name.replace('^', '_')}.dcm")
    dcmwrite(output_filename, dicom_dataset)

    print(f"DICOM dataset saved as {output_filename}")

except UnsupportedVersion:
    print("Unsupported HL7 version. Please ensure you're using a compatible version of hl7apy.")
except Exception as e:
    print("An error occurred:", e)
