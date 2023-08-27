import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dicom_dpacs.settings")
import django
django.setup()
from pynetdicom import AE, evt
from pynetdicom.sop_class import ModalityWorklistInformationFind
from pydicom.dataset import Dataset
from django.conf import settings
from Modality.models import Modality, Order
import hl7apy
import pydicom
from hl7apy.core import Segment,Message,Field
from pydicom.uid import ExplicitVRLittleEndian, generate_uid
def on_c_echo(event):
    print("Received C-ECHO request")
    return 0x0000  # Success status

def handle_mwl_query(event):
    ae = AE(ae_title='RISM')
    ae.add_requested_context(ModalityWorklistInformationFind)

    dicom_file_path = 'media/modality_worklist/DummyPatient1.dcm'
    dicom_dataset = pydicom.dcmread(dicom_file_path)
    dicom_dataset.SOPInstanceUID = generate_uid()
    dicom_dataset.SOPClassUID = '1.2.840.10008.1.1'
    modality_ip = 'localhost'
    modality_port = 11112
    
    worklist_item = Dataset()
    worklist_item.PatientName = 'Doe^John'
    worklist_item.PatientID = '12345'
    # ... Add other relevant attributes
    # print("before send")
    assoc = ae.associate(modality_ip, modality_port)
    # print("after send")
    if assoc.is_established:
        response = assoc.send_c_find(dicom_dataset, ModalityWorklistInformationFind)
        
        for (status, dataset) in response:
            if status.Status == 0x0000:
                print('Worklist item sent successfully')
                # Process the received worklist item dataset
                print(dataset,'status',status)
            else:
                print(f'Failed to send worklist item. Status: {status}')
        
        assoc.release()
    else:
        print('Failed to establish association')
def start_dicom_scp(host, port, ae_title):
    ae = AE(ae_title=ae_title)
    ae.add_supported_context(ModalityWorklistInformationFind)
    ae.add_supported_context('1.2.840.10008.1.1')

    handlers = [(evt.EVT_C_ECHO, on_c_echo),(evt.EVT_C_FIND, handle_mwl_query)]
    ae.start_server((host, port), evt_handlers=handlers)

if __name__ == "__main__":
    host = 'localhost'
    port = 11112
    ae_title = b'RIS'
    print("server is running")
    start_dicom_scp(host, port, ae_title)
