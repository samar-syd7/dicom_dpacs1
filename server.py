from pynetdicom import AE, evt,debug_logger
from pydicom import dcmread
from pydicom.dataset import Dataset
import os
import pydicom
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dicom_dpacs.settings")
import django
django.setup()
# from .serializers import StudySerializer
# from .views import getStudy
from pynetdicom.sop_class import ModalityWorklistInformationFind,ModalityPerformedProcedureStep,CTImageStorage,MRImageStorage,XRayRadiofluoroscopicImageStorage,ComputedRadiographyImageStorage
from pynetdicom.status import code_to_category
from pydicom.dataset import Dataset
from pydicom.uid import ExplicitVRLittleEndian, generate_uid
from datetime import datetime as dt
from django.http import JsonResponse
import cv2
from Modality.models import Study, Series, Image, Patient, Report, ModalitySystem, File
import random
debug_logger()

def get_random():
    return random.randint(10000,99999999)

def start_dicom_server(request):
    print("server started ==========")
    
    pacs_ip = '127.0.0.1'
    pacs_port = 9000

    ae = AE()  # Add parentheses to instantiate AE

    data_ser =  {}

    def on_c_store(event):
        print("on c store \n\n\n\n =============>")
        ds = event.dataset
        sop_class_uid = ds.SOPClassUID
        instance_uid = ds.SOPInstanceUID

        # Generate a unique filename for storing the received DICOM file
        filename = f"received_{sop_class_uid}_{instance_uid}.dcm"

        # Save the received dataset to a file
        ds.save_as(filename, write_like_original=False)



        # old ---
        ds = event.dataset   
        # for i in ds:
        #     print(i,'\n')
        
        instance_uid = ds.SOPInstanceUID

        print("-----------------")

        # Save the DICOM image to the media directory
        dicom_path = os.path.join("media/", f'{instance_uid}.dcm')
        ds.save_as(dicom_path)

        print("ds ----save")

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
        datetime = dt.strptime(study_date, "%Y%m%d")
        

        content_datetime = datetime

        procedure_start_date = ds.get("PerfProcStepStartDate", "")
        procedure_start_time = ds.get("PerfProcStepStartTime", "")
        procedure_step_id = ds.get("PerfProcStepID", "")
        procedure_step_description = ds.get("PerfProcStepDesc", "")
        
        print('patient before save')
        # Create or retrieve the Patient record
        patient = Patient(
            patient_no=get_random(),
            patient_name=patient_name,
            patient_id=patient_id,
            patient_birthdate=patient_birth_date,
            patient_sex=patient_sex,
            modality=modality,
        )
        patient.save()
        print('patient after save')
        
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

        finaldata = ModalitySystem(
            patient = patient,
            study = study,
            series = series,
            image= image
        )
        finaldata.save()

        # ae.shutdown()

        return 0x0000  # Success status
           

    def on_c_echo(event):
        print("Received C-ECHO request")
        return 0x0000  # Success status

    def handle_mwl_query(event):
        import datetime
        print("worked ---->")
        ds = event.identifier

        # modality_records = Modality.objects.all()
        # order_records = Order.objects.all()

        response_ds_list = []

        
        response_ds = ds.copy()
        response_ds.PatientID = "12345"
        response_ds.PatientName = "Fardeen Khan"
        response_ds.PatientSex = "M"
        response_ds.PatientBirthDate = datetime.date.today().strftime("%Y%m%d")
        response_ds.StudyInstanceUID = "1232232323"
        # response_ds.StationID = order.station_id
        # response_ds.RequestedProcedureID = order.requested_procedure_description
        # response_ds.StationName = modality.name
        # response_ds.RequestedProcedureDescription = order.requested_procedure_description
        # response_ds.ScheduledProcedureStepStartDate = order.patient_birth_date.strftime("%Y%m%d")
        # response_ds.ScheduledProcedureStepStartTime = order.patient_birth_date.strftime("%H%M%S")
        response_ds.Modality = "CT"
        response_ds.ScheduledStationAETitle = "CT"
        response_ds.Status = 0x0000
                
        response_ds_list.append(response_ds)
        # print(f'{response_ds}\n')
            
        # event.identifier = response_ds_list
        yield 0xFF00, response_ds

    def handle_mpps_progress(event):
        print("N -create executed")
        ds = event.request
        sop_instance_uid = ds.RequestedSOPInstanceUID
        # ... Extract other relevant data
        
        # Create an N-Create-RSP response dataset
        response = ds  # Just an example, you can create a new Dataset
        
        # Set the status of the response
        response.Status = 0x0000  # Success status

        # Send the N-Create-RSP response
        return response
    
    handlers = [
        (evt.EVT_C_STORE, on_c_store),
        (evt.EVT_C_ECHO, on_c_echo),
        (evt.EVT_C_FIND, handle_mwl_query),
        (evt.EVT_N_EVENT_REPORT, handle_mpps_progress),
        (evt.EVT_N_CREATE, handle_mpps_progress),
        (evt.EVT_N_ACTION, handle_mpps_progress),
    ]
    ae.add_supported_context('1.2.840.10008.1.1')  # Use correct UID for DICOM verification
    # 1.2.826.0.1.3680043.2.1545.6.3.1.0
    ae.add_supported_context(ModalityWorklistInformationFind)
    ae.add_supported_context('1.2.840.10008.5.1.4.1.1.7')  # DICOM image storage
    ae.add_supported_context(CTImageStorage)
    ae.add_supported_context(MRImageStorage)
    ae.add_supported_context(XRayRadiofluoroscopicImageStorage)
    ae.add_supported_context(ComputedRadiographyImageStorage)

    ae.ae_title = 'PACS'
    ae.start_server((pacs_ip, pacs_port), block=False, evt_handlers=handlers)
    print(f"PACS server listening on {pacs_ip}:{pacs_port}")
    return JsonResponse(data=data_ser,safe=True)    
start_dicom_server()