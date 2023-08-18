import socket

host = 'localhost'  # Change to the server's host
port = 9556        # Change to the server's port

hl7_message = (
        "MSH|^~\\&|5.0^QSInsight^L|^^|DBO^QSInsight^L|QS4444^^|20051019163235||VXX^V02|1129757555111.100000025|P|2.3.1|",
        "MSA|AA|QS444437861000000042||",
        "QRD|20030828104856|R|I|QueryID01|||5|10^SNOW^MARY^^^^^^^^^^SR|VXI^Vaccine Information^HL70048|SIIS|",
        "QRF|QS4444|20030828104856|20030828104856||100000001~20021223|",
        "PID|1||41565^^^^SR~2410629811:72318911||SNOW^MARY^^^^^L||20021223|F|||2 NORTH WAY RD^^MOORESVILLE^INDIANA^46158^^M||(317)123-4567^^PH||EN^English^HL70296|||||||||||||||N|",
        "PID|2||28694^^^^SR~2663391364:111111111||FROG^KERMIT^^^^^L||20021223|",
        "NK1|1|PIGGY^MISS|GRD^Guardian^HL70063|"

)

hl7_message_str = "\n".join(hl7_message)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))
client_socket.sendall(hl7_message_str.encode())
client_socket.close()

print("HL7 message sent to server")