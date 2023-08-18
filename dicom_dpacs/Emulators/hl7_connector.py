import socket

# Set the host and port for the HL7 listener
hl7_host = 'localhost'  # Change to your desired host
hl7_port = 9556         # Change to your desired port

# Create a socket for the HL7 listener
hl7_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
hl7_socket.bind((hl7_host, hl7_port))
hl7_socket.listen(1)

print(f"HL7 Listener is running on {hl7_host}:{hl7_port}")

media_folder = "media/hl7_message"  # Change to your desired media folder path

while True:
    connection, client_address = hl7_socket.accept()
    print(f"Connection from: {client_address}")
    
    hl7_message = b""
    
    try:
        print("Receiving HL7 message...")
        while True:
            data = connection.recv(1024)
            if not data:
                break
            hl7_message += data
    except Exception as e:
        print("Error while receiving data:", e)
    
    connection.close()
    
    if hl7_message:
        hl7_message_str = hl7_message.decode("utf-8")
        
        # Create a filename based on the MSH-10 field (message control ID)
        message_control_id = hl7_message_str.split("|")[9]
        message_file = f"{media_folder}/hl7_message_{message_control_id}.hl7"
        
        with open(message_file, "w") as f:
            f.write(hl7_message_str)
            print(f"HL7 message saved as: {message_file}")
