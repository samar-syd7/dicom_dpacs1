from pynetdicom import AE, QueryRetrievePresentationContexts
from pynetdicom.sop_class import ModalityWorklistInformationFind, CTImageStorage
from pydicom.dataset import Dataset

def query_worklist(ris_ip, ris_port):
    ae = AE()
    ae.add_requested_context(ModalityWorklistInformationFind)

    ris_address = (ris_ip, ris_port)

    assoc = ae.associate(ris_address)
    if assoc.is_established:

        query_dataset = Dataset()
        query_dataset.PatientName = "Tom"

        responses = assoc.send_c_find(query_dataset, ModalityWorklistInformationFind)

        for(status, dataset) in responses:
            if status:
                print("Recieved Worklist entry:")
                print(dataset)
            else:
                print("C-Find failed")
            
        assoc.release()


def send_dicom_to_pacs(pacs_ip, pacs_port):
    ae = AE()
    ae.add_requested_context(CTImageStorage)


    pacs_address = (pacs_ip, pacs_port)

    assoc = ae.associate(pacs_address)
    if assoc.is_established:

        ds = Dataset()
        ds.PatientName="Tom"
        ds.Modality="CT"
        
        status = assoc.send_c_store(ds)

        if status:
            print("DICOM Instance sent and stored succesfully")
        else:
            print("C-Store failed")
        
    assoc.release()

ris_ip='127.0.0.1'
ris_port=11112
query_worklist(ris_ip,ris_port)

pacs_ip='127.0.0.1'
pacs_port=9000
send_dicom_to_pacs(pacs_ip,pacs_port)

        

