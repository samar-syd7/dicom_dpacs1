from pynetdicom import AE, QueryRetrievePresentationContexts
from pynetdicom.sop_class import ModalityWorklistInformationFind
from pydicom.dataset import Dataset
from pydicom import dcmread
from Emulators.modality import query_worklist
import os

def create_entry():
    patient_data={
        'PatientID' : '12345',
        'PatientName' : 'Tom',
        'Modality' : 'CT'
    }

    return patient_data

def convert_into_dicom(patient_data):
    ds = Dataset()
    ds.PatientID = patient_data['PatientID']
    ds.PatientName = patient_data['PatientName']
    ds.Modality = patient_data['Modality']

    dicom_file_path = f'media/{ds.SOPInstanceUID}.dcm'
    ds.save_as(dicom_file_path)
    return dicom_file_path

patient_data = create_entry()
dicom_file_path = convert_into_dicom(patient_data)

ris_ip = '127.0.0.1'
ris_port = 11112
query_worklist(ris_ip,ris_port)


pacs_ip = '127.0.0.1'
pacs_port = 9000

ae = AE()
ae.add_requested_context('1.2.840.10008.1.1')
ae.add_requested_context('1.2.840.10008.5.1.4.1.1.7')

with ae.associate((pacs_ip,pacs_port)) as assoc:
    if assoc.is_established:
        ds = dcmread(dicom_file_path)
        status = assoc.send_c_store(ds)

        if status :
            print('DICOM instances send and saved succesfully')
        else :
            print('C-STORE failed')

os.remove(dicom_file_path)