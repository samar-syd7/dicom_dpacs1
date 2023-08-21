import pydicom
from pydicom.dataset import Dataset
from pydicom.uid import UID
from pynetdicom.sop_class import ModalityWorklistInformationFind
from pynetdicom import AE, evt
from datetime import datetime
from django.conf import settings
from Modality.models import Modality, Order

def handle_mwl_query(event):
    query_attrs = event.identifier

    modality_records = Modality.objects.all()
    order_records = Order.objects.all()

    response_ds_list = []

    for modality in modality_records:
        for order in order_records:
            response_ds = Dataset()
            response_ds.PatientID = order.patient_id
            response_ds.PatientName = order.patient_name
            response_ds.PatientSex = order.patient_sex
            response_ds.PatientDOB = order.patient_birth_date
            response_ds.Modality = modality.name
            response_ds.Description = modality.description
            response_ds.ReferencedBy = order.referring_physicians_name
            response_ds.Req_Procedure = order.requested_procedure_description
            response_ds.StudyInstanceID = order.study_instance_uid
            response_ds.Station_ID = order.station_id
            response_ds.PatientCreatedAt = order.created_at
            response_ds.PatientUpdatedAt = order.updated_at
            response_ds.ModalityCreatedAt = modality.created_at
            response_ds.ModalityUpdatedAt = modality.updated_at

            response_ds_list.append(response_ds)
            event.identifier = response_ds_list

            return 0x0000

def start_dicom_scp():
    ae = AE(ae_title=settings.DICom_SCP_AETITLE.encode())
    ae.supported_contexts = [ModalityWorklistInformationFind]

    handlers = [(evt.EVT_C_FIND, handle_mwl_query)]
    ae.start_server(("127.0.0.1", 11112), evt_handlers=handlers)

if __name__ == "__main__":
    start_dicom_scp()