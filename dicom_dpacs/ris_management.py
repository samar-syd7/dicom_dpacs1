from pynetdicom import AE, evt
from pynetdicom.sop_class import PatientRootQueryRetrieveInformationModelFind
from pydicom.dataset import Dataset

def on_c_find(event):
    print('+++++++++++++')
    ds = event.identifier

    # Perform some action based on the query dataset
    # For example, you can retrieve patients based on query parameters

    # Create a response dataset (can be empty for no matches)
    response = []
    response_item = Dataset()
    response_item.PatientName="Tom"
    response_item.Modality="CT"
    response.append(response_item)

    # Add the response dataset to the event
    event.add_response(response)

    return 0x0000

# Create an Application Entity (AE)
ae = AE(ae_title=b'RISM')

# Add the Patient Root Query/Retrieve Information Model - Find SOP Class
ae.add_supported_context(PatientRootQueryRetrieveInformationModelFind)

# Set the IP address and port of your DICOM server
server_ip = '127.0.0.1'
server_port = 11112

# Start the server and listen for C-FIND requests
handlers = [(evt.EVT_C_FIND, on_c_find)]
print("server")
ae.start_server((server_ip, server_port), block=True, evt_handlers=handlers)

