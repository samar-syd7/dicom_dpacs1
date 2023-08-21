import os
from pydicom import dcmwrite
from pydicom.dataset import Dataset
# from hl7 import parse
from hl7apy.parser import parse_message
from hl7apy.exceptions import UnsupportedVersion

print("Started....conversion")
hl7_file_path = 'media/hl7_messages/hl7_message_101109.hl7'
with open(hl7_file_path, 'r') as hl7_file:
    hl7_message_str = hl7_file.read()
    # print(hl7_message_str, "------")
    # print("\n")

try:
    # Parse the HL7 message using hl7apy
    message = (
    'MSH|^~\&|MESA_OP|XYZ_HOSPITAL|iFW|ABC_RADIOLOGY|||ORM^O01|101109|P|2.3||||||||\r'
    'PID|1||20891312^^^^EPI||APPLESEED^JOHN^A^^MR.^||19661201|M||AfrAm|505 S. HAMILTON AVE^^MADISON^WI^53505^US^^^DN |DN|(608)123-4567|(608)123-5678||S||11480003|123-45-7890||||^^^WI^^\r'
    'PD1|||FACILITY(EAST)^^12345|1173^MATTHEWS^JAMES^A^^^\r'
    'PV1|||^^^CARE HEALTH SYSTEMS^^^^^||| |1173^MATTHEWS^JAMES^A^^^||||||||||||610613||||||||||||||||||||||||||||||||V\r'
    'ORC|NW|987654^EPIC|76543^EPC||Final||^^^20140418170014^^^^||20140418173314|1148^PATTERSON^JAMES^^^^||1173^MATTHEWS^JAMES^A^^^|1133^^^222^^^^^|(618)222-1122||\r'
    'OBR|1|363463^EPC|1858^EPC|73610^X-RAY ANKLE 3+ VW^^^X-RAY ANKLE ||||||||||||1173^MATTHEWS^JAMES^A^^^|(608)258-8866||||||||Final||^^^20140418170014^^^^|||||6064^MANSFIELD^JEREMY^^^^||1148010^1A^EAST^X-RAY^^^|^|\r'
    'DG1||I10|S82^ANKLE FRACTURE^I10|ANKLE FRACTURE||'
    
)
    hl7_message = parse_message(hl7_message_str)
    hl7_message2 = parse_message(message)
    
    # print('\n\n\n\n\n',hl7_message_str,'\n\n\n\n\n',message)
    # print(hl7_message[0][0],'\n\n\n',hl7_message2[0])
    # for (index,i) in enumerate(hl7_message2._get_children('SEG')[1]):
    #     for j in i._get_children('SEG')[0]:
    #         for k in j.
    #         print(j._get_children('SEG'))
        # print(index,i._get_children('SEG')[0],'\n')
        # pas
    print(type(hl7_message2))
    print(hl7_message2._get_children('SEG')[1])
    # print(xcvxf)

    # Access the first PID segment
    pid_segment = hl7_message[0][0][3]
    print(pid_segment,'\n\n\n')

    # Accessing patient name (field index: 5)
    #patient_name = pid_segment[0][0][][][]

    # Accessing patient ID (field index: 3)
    #patient_id = pid_segment[3][0]

    # Create a Modality Worklist DICOM dataset
    dicom_dataset = Dataset()
    dicom_dataset.PatientName = patient_name
    dicom_dataset.PatientID = patient_id
    dicom_dataset.ScheduledProcedureStepDescription = "CT Abdomen"
    dicom_dataset.ScheduledProcedureStepID = "SPS123"

    output_path = "media/modality_worklist/"

    # Saving the DICOM dataset as a .dcm file
    output_filename = os.path.join(output_path, f"{patient_name.replace('^', '_')}.dcm")
    dcmwrite(output_filename, dicom_dataset)

    print(f"DICOM dataset saved as {output_filename}")

except UnsupportedVersion:
    print("Unsupported HL7 version. Please ensure you're using a compatible version of hl7apy.")
except Exception as e:
    print("An error occurred:", e)
