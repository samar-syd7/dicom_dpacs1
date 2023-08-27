from pynetdicom import AE, evt
from pydicom import dcmread
from pydicom.dataset import Dataset
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dicom_dpacs.settings")
import django
django.setup()
from Modality.models import Study, Series, Image  # Import your Django models


print('----')
def on_c_store(event):
    ds = event.dataset
    print('-=-=-=-=-=-=-=-=')
    instance_uid = ds.SOPInstanceUID
    print(instance_uid,'==')
    ds.save_as(f'media/{instance_uid}.dcm')
    print(f'Received: {instance_uid}')

    study_instance_uid = ds.StudyInstanceUID
    patient_name = ds.PatientName
    patient_id = ds.PatientID
    print("========================= before save")
    study = Study(
        study_instance_uid=study_instance_uid,
        patient_name= patient_name, patient_id=patient_id
    )
    study.save()

    return 0x0000

pacs_ip = '127.0.0.1'
pacs_port = 9000

handlers = [(evt.EVT_C_STORE, on_c_store)]

ae = AE()  # Add parentheses to instantiate AE
ae.add_supported_context('1.2.840.10008.1.1')  # Use correct UID for DICOM verification
# 1.2.826.0.1.3680043.2.1545.6.3.1.0
ae.add_supported_context('1.2.840.10008.5.1.4.1.1.7')  # DICOM image storage

ae.ae_title = 'PACS'
ae.start_server((pacs_ip, pacs_port), block=True, evt_handlers=handlers)
print(f"PACS server listening on {pacs_ip}:{pacs_port}")
