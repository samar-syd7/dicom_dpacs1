import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dicom_dpacs.settings")
import django
django.setup()
from pynetdicom import AE, evt
from pynetdicom.sop_class import ModalityWorklistInformationFind
from pydicom.dataset import Dataset
from django.conf import settings
from Modality.models import Modality, Order
import hl7apy
from hl7apy.core import Segment,Message,Field
def on_c_echo(event):
    print("Received C-ECHO request")
    return 0x0000  # Success status

def handle_mwl_query(event):
    query_attrs = event.identifier
    hl7_file_path = 'media/hl7_messages/hl7_message_101109.hl7'
    # print(hl7_message_str, "------")
    # print("\n")

    from hl7apy.parser import parse_message
    import socket
    # hl7_file_path = 'media/hl7_messages/hl7_message_101109.hl7'
    
    modality_ip = 'localhost'
    modality_port = 11112

    # Create a PID segment
    print("Before PID")
    # pid = Segment("PID")
    
    print("Before PID 2")
    m = Message("ADT_A01")

    print("Before PID 3")
    pid = Segment("PID")
    pid_5 = Field("PID_5")

    print("Before PID 4")
    pid_5.pid_5_1 = 'EVERYMAN'
    pid_5.pid_5_2 = 'ADAM'

    print("Before PID 5")
    pid.add(pid_5)
    print("Before PID 6")
    m.add(pid)
    print("After PID")

    # Convert the HL7 message to a string
    hl7_string = str(m)
    print('before connect')
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((modality_ip, modality_port))
    print('after connect')


    msh = "MSH|^~\&|GHH_ADT||||20080115153000||ADT^A01^ADT_A01|0123456789|P|2.5||||AL\r"
    evn = "EVN||20080115153000||AAA|AAA|20080114003000\r"
    pid = "PID|1||566-554-3423^^^GHH^MR||EVERYMAN^ADAM^A|||M|||2222 HOME STREET^^ANN ARBOR^MI^^USA||555-555-2004~444-333-222|||M\r"
    nk1 = "NK1|1|NUCLEAR^NELDA^W|SPO|2222 HOME STREET^^ANN ARBOR^MI^^USA\r"
    pv1 = "PV1|1|I|GHH PATIENT WARD|U||||^SENDER^SAM^^MD|^PUMP^PATRICK^P|CAR||||2|A0|||||||||||||||||||||||||||||2008\r"
    in1 = "IN1|1|HCID-GL^GLOBAL|HCID-23432|HC PAYOR, INC.|5555 INSURERS CIRCLE^^ANN ARBOR^MI^99999^USA||||||||||||||||||||||||||||||||||||||||||||444-33-3333"
    s = msh + evn + pid + nk1 + pv1 + in1
    message = parse_message(s)

    message_str = str(message.to_er7())
    print(message_str.encode(),'[][]')
    # Send the HL7 message
    client_socket.send(message_str.encode())
    print(client_socket.send(message_str.encode()),'------------',message.to_er7())

    # Close the socket connection
    client_socket.close()

    # for modality in modality_records:
    #     for order in order_records:
    #         response_ds = Dataset()
    #         response_ds.PatientID = order.patient_id
    #         response_ds.PatientName = order.patient_name
    #         response_ds.RequestedProcedureID = order.requested_procedure_description
    #         response_ds.ScheduledProcedureStepStartDate = order.patient_birth_date.strftime("%Y%m%d")
    #         response_ds.Modality = modality.name
    #         response_ds.ScheduledStationAETitle = "CT"
            
    #         response_ds_list.append(response_ds)
    #         # print(f'{response_ds}\n')
    
    print(type(hl7_string.encode()))
    # event.body = hl7_string.encode()
    # print(hl7_string)
    event.identifier = message_str.encode()
    print('---before send')
    return message_str.encode(),0x0000

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
