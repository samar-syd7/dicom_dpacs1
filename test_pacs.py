import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dicom_dpacs.settings")
import django
django.setup()

from datetime import datetime as dt
from pydicom.uid import generate_uid
from pynetdicom import AE, evt, debug_logger
from pynetdicom.sop_class import CTImageStorage
from django.conf import settings
from Modality.models import Study, Series, Image, Patient, Report, ModalitySystem, File

import random
def get_random():
    return random.randint(10000,99999999)

debug_logger()

def handle_c_store(event):
    ds = event.dataset   
    # for i in ds:
    #     print(i,'\n')
    
    instance_uid = ds.SOPInstanceUID

    # Save the DICOM image to the media directory
    dicom_path = os.path.join(settings.MEDIA_ROOT, f'{instance_uid}.dcm')
    ds.save_as(dicom_path)

    # Create or retrieve Study and Series records in your database
    study_instance_uid = generate_uid()
    # patient_no = get_random()
    # patient_id = ds.PatientID
    # patient_birth_date = ds.PatientBirthDate
    # patient_sex = ds.PatientSex

    study_date = ds.StudyDate
    study_time = ds.StudyTime
    accession_number = ds.AccessionNumber
    modality = ds.Modality
    study_description = ds.StudyDescription
    series_description = ds.SeriesDescription
    performing_physician = ds.get("PerfPhys", "")
    operators_name = ds.get("OperatorsName", "")
    patient_name = ds.PatientName
    patient_id = ds.PatientID
    patient_birth_date = ds.PatientBirthDate
    patient_sex = ds.PatientSex
    study_instance_uid = ds.StudyInstanceUID
    series_instance_uid = ds.SeriesInstanceUID
    study_id = ds.StudyID
    series_number = ds.SeriesNumber
    instance_number = ds.InstanceNumber
    rows = ds.Rows
    columns = ds.Columns
    bits_allocated = ds.BitsAllocated
    bits_stored = ds.BitsStored
    high_bit = ds.HighBit
    pixel_representation = ds.PixelRepresentation
    content_datetime_str = f"{study_date} {study_time}"
    content_datetime = dt.strptime(content_datetime_str, "%Y%m%d %H%M%S")

    procedure_start_date = ds.get("PerfProcStepStartDate", "")
    procedure_start_time = ds.get("PerfProcStepStartTime", "")
    procedure_step_id = ds.get("PerfProcStepID", "")
    procedure_step_description = ds.get("PerfProcStepDesc", "")
    
    # Create or retrieve the Patient record
    patient = Patient(
        PatientNo=get_random(),
        PatientName=patient_name,
        PatientID=patient_id,
        PatientBirthDate=patient_birth_date,
        PatientSex=patient_sex
    )
    patient.save()
    
    # Create the Study record 
    study_instance_uid = generate_uid()
    study = Study(
        study_instance_uid=study_instance_uid,
        PatientNo=patient,
        accession_no=accession_number,
        study_description=study_description,
        study_no=study_id
    )
    study.save()

    # Create the Series record
    series_instance_uid = generate_uid()
    series = Series(
        series_instance_uid=series_instance_uid,
        study_no=study,
        series_no=series_number,
        series_number=series_number,
        accession_no=accession_number,
        series_description=series_description,
    )
    series.save()

    # Save the Image record in your database
    image = Image(
        series=series,
        sop_instance_uid=instance_uid,
        modality=modality,
        instance_number=instance_number,
        content_datetime=content_datetime,
        samples_per_pixel=ds.get("SamplesPerPixel", ""),
        photometric_interpretation=ds.get("PhotometricInterpretation", ""),
        rows=rows,
        columns=columns,
        bits_allocated=bits_allocated,
        bits_stored=bits_stored,
        high_bit=high_bit,
        pixel_representation=pixel_representation,
        image=dicom_path,
    )
    image.save()

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
