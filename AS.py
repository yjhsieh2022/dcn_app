from socket import *

server_port = 53533
server_socket = socket(AF_INET, SOCK_DGRAM)
server_socket.bind(('', server_port))
mappings = {}

print("The AS server is ready to receive message")
while True:
    message, client_address = server_socket.recvfrom(2048)
    msg_decoded = message.decode()
    print("got the message: " + msg_decoded)

    if "VALUE" in msg_decoded:
        print("registeration request is taken")
        splitted = msg_decoded.split("\n")
        name = splitted[1].split("=")[1]
        value = splitted[2].split("=")[1]
        mappings[name] = value
        print("Name: {} Value: {}".format(name, value))
        server_socket.sendto("Success".encode(), client_address)
    else:
        print("query request is taken")
        splitted = msg_decoded.split("\n")
        name = splitted[1].split("=")[1]
        print("Name: {}".format(name))
        if name in mappings:
            response = "TYPE=A\nNAME={}\nVALUE={}\nTTL=10".format(name, mappings[name])
            server_socket.sendto(response.encode(), client_address)