# this is to connect with modality and send worklist

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dicom_dpacs.settings")
import django
django.setup()
from pynetdicom import AE, evt
from pynetdicom.sop_class import ModalityWorklistInformationFind
from pydicom.dataset import Dataset
from django.conf import settings
from Modality.models import Order

def on_c_echo(event):
    print("Received C-ECHO request")
    return 0x0000  # Success status

def handle_mwl_query(event):
    query_attrs = event.identifier
    
    order_records = Order.objects.all()

    response_ds_list = []

    for order in order_records:
            response_ds = Dataset()
            response_ds.PatientID = order.patient_id
            response_ds.PatientName = order.patient_name
            #response_ds.PatientSex = order.patient_sex
            #response_ds.PatientBirthDate = order.patient_birth_date.strftime("%Y%m%d")
            # response_ds.StudyInstanceUID = order.study_instance_uid
            # response_ds.StationID = order.station_id
            response_ds.RequestedProcedureID = order.requested_procedure_description
            # response_ds.StationName = modality.name
            # response_ds.RequestedProcedureDescription = order.requested_procedure_description
            response_ds.ScheduledProcedureStepStartDate = order.patient_birth_date.strftime("%Y%m%d")
            # response_ds.ScheduledProcedureStepStartTime = order.patient_birth_date.strftime("%H%M%S")
            response_ds.Modality = "CR"
            response_ds.ScheduledStationAETitle = "CT"
            
            response_ds_list.append(response_ds)
            print(f'{response_ds}\n')
        
    event.identifier = response_ds_list
    return 0x0000

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
