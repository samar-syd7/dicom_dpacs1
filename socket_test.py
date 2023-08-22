from hl7apy.parser import parse_message
import socket
hl7_file_path = 'media/hl7_messages/hl7_message_101109.hl7'
with open(hl7_file_path, 'r') as hl7_file:
    hl7_content  = hl7_file.read()
hl7_message = parse_message(hl7_content)
modality_ip = 'localhost'
modality_port = 11112

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((modality_ip, modality_port))
hl7_string = str(hl7_message)
client_socket.send(hl7_string.encode())
client_socket.close()


