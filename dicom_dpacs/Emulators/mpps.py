from pydicom.dataset import Dataset
from pydicom.uid import generate_uid
from pynetdicom import AE, evt
from pynetdicom.sop_class import ModalityPerformedProcedureStep
from pynetdicom.status import code_to_category

# Modify the IP address and port according to the remote MPPS modality emulator
remote_address = "127.0.0.1"
remote_port = 11112

# Generate unique UIDs
ct_study_uid = generate_uid()
mpps_instance_uid = generate_uid()

# Our N-CREATE *Attribute List*
def build_attr_list():
    # ... (same as in your original code)

# Our N-SET *Modification List*
def build_mod_list(series_instance, sop_instances):
    # ... (same as in your original code)

# Our final N-SET *Modification List*
    final_ds = Dataset()
    final_ds.PerformedProcedureStepStatus = "COMPLETED"
    final_ds.PerformedProcedureStepEndDate = "20000101"
    final_ds.PerformedProcedureStepEndTime = "1300"

# Implement the evt.EVT_N_CREATE handler
def handle_create(event):
    # ... (same as in your original code)

# Implement the evt.EVT_N_SET handler
def handle_set(event):
    # ... (same as in your original code)

# Define event handlers
    handlers = [(evt.EVT_N_CREATE, handle_create), (evt.EVT_N_SET, handle_set)]

# Initialise the Application Entity and specify the listen port
    ae = AE()

# Add the supported presentation context
    ae.add_supported_context(ModalityPerformedProcedureStep)

# Start listening for incoming association requests
    ae.start_server(("127.0.0.1", 11112), evt_handlers=handlers)

# Associate with the remote MPPS modality emulator
    assoc = ae.associate(remote_address, remote_port)

    if assoc.is_established:
    # Use the N-CREATE service to send a request to create a SOP Instance
        status, attr_list = assoc.send_n_create(
            build_attr_list(),
            ModalityPerformedProcedureStep,
            mpps_instance_uid
        )

    if status:
        print('N-CREATE request status: 0x{0:04x}'.format(status.Status))
        category = code_to_category(status.Status)
        if category in ['Warning', 'Success']:
            print(attr_list)
            
            # Use the N-SET service to update the SOP Instance
            status, attr_list = assoc.send_n_set(
                build_mod_list(ct_series_uid, ct_instance_uids),
                ModalityPerformedProcedureStep,
                mpps_instance_uid
            )

            if status:
                print('N-SET request status: 0x{0:04x}'.format(status.Status))
                category = code_to_category(status.Status)
                if category in ['Warning', 'Success']:
                    # Send completion
                    status, attr_list = assoc.send_n_set(
                        final_ds,
                        ModalityPerformedProcedureStep,
                        mpps_instance_uid
                    )
                    if status:
                        print('Final N-SET request status: 0x{0:04x}'.format(status.Status))
        else:
            print('Connection timed out, was aborted or received invalid response')

            assoc.release()
    else:
        print('Association rejected, aborted or never connected')
