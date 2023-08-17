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
def on_c_echo(event):
    print("Received C-ECHO request")
    return 0x0000  # Success status

def send_response_to_modality(response):
    # Set the modality emulator's IP and port
    modality_ip = 'localhost'
    modality_port = 11112  # Replace with the actual port
    
    ae = AE(ae_title=b'MODALITY')
    assoc = ae.associate(modality_ip, modality_port)
    
    if assoc.is_established:
        # Send the response data
        status = assoc.send_c_find_response(response, 0x0000)
        
        # Release the association
        assoc.release()
    else:
        print("Failed to establish association with modality emulator")


def on_c_find(event):
    print("Received C-FIND request")
    response = []
    response_item = Dataset()
    response_item.PatientName = 'Doe^John'
    response_item.PatientID = '12345'
    response_item.Modality = 'CT'
    response_item.ScheduledProcedureStepDescription = 'CT Abdomen'
    response.append(response_item)
    event.add_response(response)
    send_response_to_modality(response)
    return response,0x0000  # Completed status

def start_dicom_server(host, port, ae_title):
    ae = AE(ae_title=ae_title)
    
    ae.add_supported_context(ModalityWorklistInformationFind)
    ae.add_supported_context('1.2.840.10008.1.1')  # Verification SOP Class

    handlers = [(evt.EVT_C_ECHO, on_c_echo), (evt.EVT_C_FIND, on_c_find)]
    ae.start_server((host, port), block=True, evt_handlers=handlers)

if __name__ == '__main__':
    host = 'localhost'
    port = 11112
    ae_title = b'RISM'
    print("server is running")
    start_dicom_server(host, port, ae_title)
