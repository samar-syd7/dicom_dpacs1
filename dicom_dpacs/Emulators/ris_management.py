# from pynetdicom import AE, evt
# from pynetdicom.sop_class import PatientRootQueryRetrieveInformationModelFind
# from pydicom.dataset import Dataset

# def on_c_find(event):
#     print('+++++++++++++')
#     ds = event.identifier

#     # Perform some action based on the query dataset
#     # For example, you can retrieve patients based on query parameters

#     # Create a response dataset (can be empty for no matches)
#     response = []
#     response_item = Dataset()
#     response_item.PatientName="Tom"
#     response_item.Modality="CT"
#     response.append(response_item)

#     # Add the response dataset to the event
#     event.add_response(response)

#     return 0x0000

# # Create an Application Entity (AE)
# ae = AE(ae_title=b'RISM')

# # Add the Patient Root Query/Retrieve Information Model - Find SOP Class
# ae.add_supported_context(PatientRootQueryRetrieveInformationModelFind)
# ae.add_requested_context('1.2.840.10008.5.1.4.31')

# # Set the IP address and port of your DICOM server
# server_ip = '127.0.0.1'
# server_port = 11112

# # Start the server and listen for C-FIND requests
# handlers = [(evt.EVT_C_FIND, on_c_find)]
# print("server")
# ae.start_server((server_ip, server_port), block=True, evt_handlers=handlers)




# from pynetdicom import AE, VerificationPresentationContexts

# def perform_dicom_echo(host, port, ae_title):
#     ae = AE(ae_title=b'RISM')
#     for context in VerificationPresentationContexts:
#         ae.add_requested_context(context.abstract_syntax)
    
#     assoc = ae.associate(host, port)
#     if assoc.is_established:
#         status = assoc.send_c_echo()
#         assoc.release()
#         return status
#     else:
#         print("Association rejected or unable to establish.")
#         return None

# if __name__ == '__main__':
#     host = 'localhost'
#     port = 11112
#     ae_title = b'RISM'
    
#     status = perform_dicom_echo(host, port, ae_title)
#     if status is not None and status.Status == 0:
#         print("DICOM Echo successful!")
#     else:
#         print(f"DICOM Echo failed with status: {status.Status if status else 'N/A'}")

from pynetdicom import AE, evt, QueryRetrievePresentationContexts
from pynetdicom.sop_class import ModalityWorklistInformationFind
from pydicom.dataset import Dataset
import socket
def on_c_echo(event):
    print("Received C-ECHO request")
    return 0x0000  # Success status

# def send_response_to_modality(response):
#     # Set the modality emulator's IP and port
#     modality_ip = 'localhost'
#     modality_port = 11112  # Replace with the actual port
    
#     ae = AE(ae_title=b'MODALITY')
#     assoc = ae.associate(modality_ip, modality_port)
    
#     if assoc.is_established:
#         # Send the response data
#         status = assoc.send_c_find_response(response, 0x0000)
        
#         # Release the association
#         assoc.release()
#     else:
#         print("Failed to establish association with modality emulator")

# def send_hl7_worklist():
#     # Set the modality emulator's IP and port
#     modality_ip = 'localhost'
#     modality_port = 11112  # Replace with the actual port
    
#     # Read the HL7 message from a file
#     hl7_message_path = 'media/hl7_message_1129757555111.100000025.hl7'
#     with open(hl7_message_path, 'r') as hl7_file:
#         hl7_message = hl7_file.read()
    
#     ae = AE(ae_title=b'RIS')
#     assoc = ae.associate(modality_ip, modality_port)
    
#     if assoc.is_established:
#         # Send the HL7 message as a worklist to the modality
#         assoc.send_hl7_message(hl7_message.encode())
        
#         # Release the association
#         assoc.release()
#     else:
#         print("Failed to establish association with modality emulator")

# def send_hl7_message(host, port, hl7_message):
#     try:
#         with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#             s.connect((host, port))
#             s.sendall(hl7_message.encode())
#             response = s.recv(1024)  # Receive response from the modality emulator
#             print("HL7 message sent successfully")
#     except Exception as e:
#         print(f"Failed to send HL7 message: {e}")


# def on_c_find(event):
    print("Received C-FIND request")
    # response = []
    # response_item = Dataset()
    # response_item.PatientName = 'Doe^John'
    # response_item.PatientID = '12345'
    # response_item.Modality = 'CT'
    # response_item.ScheduledProcedureStepDescription = 'CT Abdomen'
    # response.append(response_item)
    # event.add_response(response)
    
    hl7_message_path = 'media/hl7_messages/hl7_message_1129757555111.100000025.hl7'
    with open(hl7_message_path, 'r') as hl7_file:
        hl7_message = hl7_file.read()
    
    modality_ip = 'localhost'
    modality_port = 11112  # Replace with the actual port
    
    send_hl7_message(modality_ip, modality_port, hl7_message)
    
    return [], 0x0000  # Completed status

def send_dicom_worklist(modality_ip, modality_port, dicom_dataset):
    ae = AE(ae_title=b'RISM')
    assoc = ae.associate((modality_ip, modality_port))

    if assoc.is_established:
        status = assoc.send_c_find_request(
            dicom_dataset, ModalityWorklistInformationFind
        )
        assoc.release()
        return status
    else:
        print("Failed to establish association with modality emulator")
        return None

def create_dicom_worklist(patient_name, patient_id, scheduled_station_ae_title, accession_number, modality):
    dicom_dataset = Dataset()
    dicom_dataset.PatientName = patient_name
    dicom_dataset.PatientID = patient_id
    dicom_dataset.ScheduledStationAETitle = scheduled_station_ae_title
    dicom_dataset.AccessionNumber = accession_number
    dicom_dataset.Modality = modality
    # Add more attributes as needed
    
    return dicom_dataset

def on_c_find(event):
    print("Received C-FIND request")
    
    # Load the attributes from your HL7 message
    patient_name = "APPLESEED^JOHN^A^^MR.^"
    patient_id = "20891312^^^^EPI"
    scheduled_station_ae_title = "ABC_RADIOLOGY"
    accession_number = "363463^EPC"
    modality = "X-RAY ANKLE 3+ VW"
    
    # Create the DICOM worklist dataset
    dicom_dataset = create_dicom_worklist(
        patient_name, patient_id, scheduled_station_ae_title, accession_number, modality
    )
    
    # Send the DICOM worklist item
    modality_ip = 'localhost'
    modality_port = 11112  # Replace with the actual port
    status = send_dicom_worklist(modality_ip, modality_port, dicom_dataset)
    
    return [], status

def start_dicom_server(host, port, ae_title):
    ae = AE(ae_title=ae_title)
    
    ae.add_supported_context(ModalityWorklistInformationFind)
    ae.add_supported_context('1.2.840.10008.1.1')  # Verification SOP Class

    handlers = [(evt.EVT_C_ECHO, on_c_echo), (evt.EVT_C_FIND, on_c_find)]
    ae.start_server((host, port), block=True, evt_handlers=handlers)

if __name__ == '__main__':
    host = 'localhost'
    port = 11112
    ae_title = b'RIS'
    print("server is running")
    start_dicom_server(host, port, ae_title)
