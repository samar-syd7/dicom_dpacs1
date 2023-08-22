from pynetdicom import AE, evt, QueryRetrievePresentationContexts
from pynetdicom.sop_class import ModalityWorklistInformationFind
from pydicom.dataset import Dataset
import socket
def on_c_echo(event):
    print("Received C-ECHO request")
    return 0x0000  # Success status

# def send_dicom_worklist(modality_ip, modality_port, dicom_dataset):
#     ae = AE(ae_title=b'RIS')
#     assoc = ae.associate((modality_ip, modality_port))

#     if assoc.is_established:
#         status = assoc.send_c_find_request(
#             dicom_dataset, ModalityWorklistInformationFind
#         )
#         assoc.release()
#         return status
#     else:
#         print("Failed to establish association with modality emulator")
#         return None

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
    modality = "XRAY_ANKLE"
    
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
