from pynetdicom import AE,evt
from pydicom.uid import ExplicitVRLittleEndian, generate_uid
# def handle_mwl_query(event):
#     import pydicom
#     from pydicom.uid import ExplicitVRLittleEndian, generate_uid
#     print("----")
#     dicom_file_path = 'media/modality_worklist/DummyPatient1.dcm'
#     dicom_dataset = pydicom.dcmread(dicom_file_path)
#     dicom_dataset.SOPInstanceUID = generate_uid()
#     dicom_dataset.SOPClassUID = '1.2.840.10008.1.1'
#     modality_ip = 'localhost'
#     modality_port = 11112

#     ae = AE(ae_title="RISM")
#     ae.add_requested_context('1.2.840.10008.1.1')
#     ae.add_requested_context('1.2.840.10008.5.1.4.31')
#     print("ae data")
#     assoc = ae.associate(modality_ip, modality_port)
#     print("assoc impl")
#     if assoc.is_established:
#         print("assoc established")
#         # print(assoc.send_c_store(dicom_dataset))
#         # print(dicom_dataset,type(dicom_dataset))
#         status = assoc.send_c_store(dicom_dataset)
#         print("Before send")
#         # assoc.release()
#         if status:
#             print('DICOM file sent successfully')
#         else:
#             print('Failed to send DICOM file')
#         assoc.release()
#         # event.identifier = dicom_dataset
#         return 0x0000
#     else:
#         print(assoc.is_established,assoc)
# from Modality.models import Modality, Order


# import hl7apy
# from hl7apy.core import Segment,Message,Field
# def handle_mwl_query(event):
#     # print(hl7_message_str, "------")
#     # print("\n")

#     from hl7apy.parser import parse_message
#     import socket
#     # hl7_file_path = 'media/hl7_messages/hl7_message_101109.hl7'
    
#     modality_ip = 'localhost'
#     modality_port = 11112

#     # Create a PID segment
#     print("Before PID")
#     # pid = Segment("PID")
    
#     print("Before PID 2")
#     m = Message("ADT_A01")

#     print("Before PID 3")
#     pid = Segment("PID")
#     pid_5 = Field("PID_5")

#     print("Before PID 4")
#     pid_5.pid_5_1 = 'EVERYMAN'
#     pid_5.pid_5_2 = 'ADAM'

#     print("Before PID 5")
#     pid.add(pid_5)
#     print("Before PID 6")
#     m.add(pid)
#     print("After PID")

#     # Convert the HL7 message to a string
#     hl7_string = str(m)
#     print('before connect')
#     client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     client_socket.connect((modality_ip, modality_port))
#     print('after connect')

#     msh ="MSH|^~\&|MESA_OF|XYZ_RADIOLOGY|MESA_IM|XYZ_IMAGE_MANAGER|201605111512||ORM^O01|100112|P|2.3.1|||||| ||"
#     pid ="PID|||M4001^^^ADT1||KING^MARTIN||19450804|M||WH|820 JORIE BLVD^^CHICAGO^IL^60523|||||||20-98-4000|||||||||||||||||||||"
#     pv1 ="PV1||E|ED||||1234^WEAVER^TIMOTHY^P^^DR|5101^NELL^FREDERICK^P^^DR|0000^Consulting^Doctor^P^^DR|HSR|||||AS||0000^Admitting^Doctor^P^^DR||V100^^^ADT1|||||||||||||||||||||||||200008201100|||||||V|"
#     orc ="ORC|NW|A100Z^MESA_ORDPLC|B100Z^MESA_ORDFIL||SC||1^once^^^^S||200008161510|^ROSEWOOD^RANDOLPH||7101^ESTRADA^JAIME^P^^DR|Enterer^^Location^EL^00000|(314)555-1212|200008161510||922229-10^IHE-RAD^IHE-CODE-231||"
#     obr ="OBR|1|A100Z^MESA_ORDPLC|B100Z^MESA_ORDFIL|P1^Procedure 1^ERL_MESA^X1_A1^SP Action Item X1_A1^DSS_MESA|||||||||xxx||Radiology^^^^R|7101^ESTRADA^JAIME^P^^DR||$ACCESSION_NUMBER$|$REQUESTED_PROCEDURE_ID$|$SCHEDULED_PROCEDURE_STEP_ID$||||MR|||1^once^^^^S|||WALK|||||||||||A|||$PROCEDURE_CODE$"
#     zds ="ZDS|1.2.4.0.13.1.432252867.1552647.1^100^Application^DICOM"
#     s = msh + pid + pv1 + orc + obr + zds
#     message = parse_message(s)

#     message_str = str(message.to_er7())
#     print(message_str.encode(),'[][]')
#     # Send the HL7 message
#     status = client_socket.send(message_str.encode())
#     print(status,'===============')
#     print(client_socket.send(message_str.encode()),'------------',message.to_er7())

#     # Close the socket connection
#     client_socket.close()

    
#     print(type(hl7_string.encode()))
#     # event.body = hl7_string.encode()
#     # print(hl7_string)
#     # event.identifier = message_str.encode()
#     print('---before send')
#     return message_str.encode(),0x0000


# handle_mwl_query(evt.EVT_C_FIND)



from pynetdicom import AE, StoragePresentationContexts
from pynetdicom.sop_class import ModalityWorklistInformationFind
from pydicom.dataset import Dataset

def send_worklist_item():
    ae = AE(ae_title='RISM')
    
    # Add the appropriate Presentation Contexts for C-FIND
    ae.add_requested_context(ModalityWorklistInformationFind)
    
    # Define the modality emulator's IP address and port
    modality_ip = 'localhost'
    modality_port = 11112
    
    # Create a worklist item (you can customize this part)
    worklist_item = Dataset()
    worklist_item.PatientName = 'Doe^John'
    worklist_item.PatientID = '12345'
    # ... Add other relevant attributes
    
    # Establish an association with the modality
    assoc = ae.associate(modality_ip, modality_port)
    
    if assoc.is_established:
        # Send the C-FIND request with the worklist item
        response = assoc.send_c_find(worklist_item, ModalityWorklistInformationFind)
        
        for (status, dataset) in response:
            if status.Status == 0x0000:
                print('Worklist item sent successfully')
                # ... Process the response dataset if needed
            else:
                print(f'Failed to send worklist item. Status: {status}')
        
        assoc.release()
    else:
        print('Failed to establish association')

if __name__ == '__main__':
    send_worklist_item()
