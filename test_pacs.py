# pacs_server.py
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dicom_dpacs.settings")
import django
django.setup()

from pynetdicom import AE, evt
from pynetdicom.sop_class import CTImageStorage
from django.conf import settings
from Modality.models import Study, Series, Image  # Import your Django models

def handle_c_store(event):
    ds = event.dataset
    instance_uid = ds.SOPInstanceUID
    print("========================= c store")

    # Save the DICOM image to the media directory
    dicom_path = f'media/{instance_uid}.dcm'
    ds.save_as(dicom_path)

    print("========================= after conversion")
    # Create or retrieve Study and Series records in your database
    study_instance_uid = ds.StudyInstanceUID
    patient_name = ds.PatientName
    patient_id = ds.PatientID
    print("========================= before save")
    study = Study(
        study_instance_uid=study_instance_uid,
        patient_name= patient_name, patient_id=patient_id
    )
    study.save()
    series_instance_uid = ds.SeriesInstanceUID

    series, created = Series.objects.get_or_create(
        series_instance_uid=series_instance_uid, study=study
    )

    # Save the Image record in your database
    image = Image(series=series, dicom_path=dicom_path)
    image.save()

    return 0x0000  # Success status

def start_dicom_scp(host, port, ae_title):
    ae = AE(ae_title=ae_title)
    ae.add_supported_context(CTImageStorage)  # Add other SOP classes as needed

    handlers = [(evt.EVT_C_STORE, handle_c_store)]
    ae.start_server((host, port), evt_handlers=handlers)

if __name__ == "__main__":
    host = 'localhost'
    port = 9000
    ae_title = b'PACS'
    print("PACS server is running")
    start_dicom_scp(host, port, ae_title)
