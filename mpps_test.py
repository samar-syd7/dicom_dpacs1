import logging
from pynetdicom import AE, evt, PYNETDICOM_IMPLEMENTATION_UID
from pydicom.dataset import Dataset
from pynetdicom.sop_class import ModalityPerformedProcedureStep
from pydicom.uid import generate_uid


logging.basicConfig(level=logging.DEBUG)
# Define a function to handle the MPPS events
print("++++++++++++++++++++")
def handle_n_create(event):
    """Handle N-Create MPPS event."""
    print("handle executed =====>")
    ct_study_uid = generate_uid()
    ds = event.request
    ds = Dataset()
    ds.ScheduledStepAttributesSequence = [Dataset()]
    step_seq = ds.ScheduledStepAttributesSequence
    step_seq[0].StudyInstanceUID = ct_study_uid
    step_seq[0].ReferencedStudySequence = []
    step_seq[0].AccessionNumber = '1'
    step_seq[0].RequestedProcedureID = "1"
    step_seq[0].RequestedProcedureDescription = 'Some procedure'
    step_seq[0].ScheduledProcedureStepID = "1"
    step_seq[0].ScheduledProcedureStepDescription = 'Some procedure step'
    step_seq[0].ScheduledProcedureProtocolCodeSequence = []
    ds.PatientName = 'Test^Test'
    ds.PatientID = '123456'
    ds.PatientBirthDate = '20000101'
    ds.PatientSex = 'O'
    ds.ReferencedPatientSequence = []
    # Performed Procedure Step Information
    ds.PerformedProcedureStepID = "1"
    ds.PerformedStationAETitle = 'SOMEAE'
    ds.PerformedStationName = 'Some station'
    ds.PerformedLocation = 'Some location'
    ds.PerformedProcedureStepStartDate = '20000101'
    ds.PerformedProcedureStepStartTime = '1200'
    ds.PerformedProcedureStepStatus = 'IN PROGRESS'
    ds.PerformedProcedureStepDescription = 'Some description'
    ds.PerformedProcedureTypeDescription = 'Some type'
    ds.PerformedProcedureCodeSequence = []
    ds.PerformedProcedureStepEndDate = None
    ds.PerformedProcedureStepEndTime = None
    # Image Acquisition Results
    ds.Modality = 'CT'
    ds.StudyID = "1"
    ds.PerformedProtocolCodeSequence = []
    ds.PerformedSeriesSequence = []
    print("Received N-Create MPPS event.")
    print("=========== PRINTING DS ============")
    # response = ds  # Just an example, you can create a new Dataset
        
    # Set the status of the response
    ds.Status = 0x0000  # Success status

    # Send the N-Create-RSP response
    handle_n_set(event)
    return ds,0x0000

print("-------------------------")
def handle_n_set(event):
    print("******************** Func Call \n\n\n")
    """Handle N-Set MPPS event."""
    ds = event.request
    print("Received N-Set MPPS event.")
    # Handle N-Set event (e.g., update database)
    # Respond with a status dataset
    status = 0x0000  # Success
    return status

# Application Entity (AE)
ae = AE()
ae.ae_title=b'MPPS'

# Add requested context might give error so i use supported context instead for MPPS SOP Class
transfer_syntaxes = ['1.2.840.10008.1.2']  # Define the transfer syntax(es) you support
ae.add_supported_context(ModalityPerformedProcedureStep, transfer_syntaxes)
handler =  [
    (evt.EVT_N_SET, handle_n_set),
    (evt.EVT_N_CREATE, handle_n_create),
]
ae.supported_events = handler

# Set AE implementation UID
ae.implementation_uid = PYNETDICOM_IMPLEMENTATION_UID

# Start the AE's SCP
scp_port = 4556  # SCP listening port
ae.start_server(('localhost', scp_port), block=True, evt_handlers=handler)
