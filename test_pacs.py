import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dicom_dpacs.settings")
import django
django.setup()

from pydicom.uid import generate_uid
from pynetdicom import AE, evt, debug_logger
from pynetdicom.sop_class import CTImageStorage
from django.conf import settings
from Modality.models import Study, Series, Image, Patient, Report, ModalitySystem, File

import random
def get_random():
    return random.randint(10000,99999999)

# debug_logger()

def handle_c_store(event):
    ds = event.dataset   
    for i in ds:
        print(i,'\n')
    
    instance_uid = ds.SOPInstanceUID

    # Save the DICOM image to the media directory
    dicom_path = os.path.join(settings.MEDIA_ROOT, f'{instance_uid}.dcm')
    ds.save_as(dicom_path)

    # Create or retrieve Study and Series records in your database
    study_instance_uid = generate_uid()
    patient_no = get_random()
    patient_id = ds.PatientID
    patient_birth_date = ds.PatientBirthDate
    patient_sex = ds.PatientSex
    

    # Create or retrieve the Patient record
    patient= Patient(
        PatientNo=patient_no,
        PatientName=ds.PatientName,
        PatientID=patient_id,
        PatientBirthDate =patient_birth_date,
        PatientSex =patient_sex
    )
    patient.save()
    
    # Create the Study record 
    accession_no = ds.AccessionNumber
    study_description = ds.StudyDescription
    study_no = get_random()
       
    study = Study(
        study_instance_uid=study_instance_uid,
        PatientNo_id= ds.PatientID,
        accession_no = accession_no,
        study_description = study_description,
        study_no = study_no,        
    )
    study.save()

    # Create the Series record
    series_instance_uid = generate_uid()
    series_no = ds.SeriesNumber
    series_number = get_random()
    series_description = ds.SeriesDescription
    series = Series(
        series_instance_uid=series_instance_uid,
        study_no=study_no,
        series_no=series_no,
        series_number = series_number,
        accession_no = accession_no,
        series_description = series_description,
        
        
    ).save()

    # Save the Image record in your database
    image = Image(
        series=series,
        sop_instance_uid=instance_uid,
        #modality=ds.Modality,
        
    ).save()

    return 0x0000  # Success status

def start_dicom_scp(host, port, ae_title):
    ae = AE(ae_title=ae_title)
    ae.add_supported_context('1.2.840.10008.1.1')
    ae.add_supported_context(CTImageStorage)  # Add other SOP classes as needed
    ae.add_supported_context('1.2.840.10008.5.1.4.1.1.7')

    handlers = [(evt.EVT_C_STORE, handle_c_store)]
    ae.start_server((host, port), evt_handlers=handlers)

if __name__ == "__main__":
    host = 'localhost'
    port = 9000
    ae_title = b'PACS'
    print("PACS server is running")
    start_dicom_scp(host, port, ae_title)
