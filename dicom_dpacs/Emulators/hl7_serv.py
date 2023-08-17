import datetime

from pynetdicom import AE, evt
from pydicom.dataset import Dataset
from hl7apy.core import Message, Segment, Field

# Create a sample HL7 worklist message
def create_dummy_hl7_message():
    hl7_message = Message("ORM_O01")
    
    # MSH segment
    msh = Segment("MSH")
    msh.MSH_9 = "ORM^O01"
    msh.MSH_10 = "MSG00001"
    hl7_message.add(msh)
    
    # PID segment
    pid = Segment("PID")
    pid.PID_3 = Field("123456")
    pid.PID_5[0][0] = "Doe"
    pid.PID_5[0][1] = "John"
    hl7_message.add(pid)
    
    # ORC segment
    orc = Segment("ORC")
    orc.ORC_16 = Field("CT Abdomen")
    hl7_message.add(orc)
    
    return hl7_message

# Rest of the code remains the same

    
    return hl7_message

# Send HL7 message to Modality Worklist SCP
def send_hl7_message():
    hl7_message = create_dummy_hl7_message()
    hl7_string = hl7_message.to_er7()
    
    assoc = ae.associate('localhost', 11112)  # Replace with the SCP's IP and port
    if assoc.is_established:
        response, _ = assoc.send_c_find(hl7_string, query_model="W")
        for (status, dataset) in response:
            if status.Status == 0:
                print("Received worklist entry:", dataset)
            else:
                print("Worklist query failed:", status)
        assoc.release()

# Create an Application Entity (AE) for the DICOM C-FIND SCU
ae = AE(ae_title=b"RISM")
ae.add_requested_context('1.2.840.10008.5.1.4.31')  # Modality Worklist Information Model - FIND

if __name__ == "__main__":
    send_hl7_message()
