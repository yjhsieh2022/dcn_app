from flask import Flask, request, jsonify
from socket import *
import logging

app = Flask(__name__)
logging.getLogger().setLevel(logging.DEBUG)

def fibonacci_calc(n):
    if n < 0:
        logging.info("number should be gr8 than 0")
    elif n == 1:
        return 0
    elif n == 2:
        return 1
    else:
        return fibonacci_calc(n - 1) + fibonacci_calc(n - 2)

@app.route('/fibonacci', methods=['GET'])
def fibonacci():
    number = request.args.get('number')
    if not number:
        return jsonify('number is not provoided'), 400
    
    logging.info("request received for Fib sequence number: {}".format(number))
    return jsonify(fibonacci_calc(int(number))), 200

@app.route('/register', methods=['PUT'])
def register():
    data = request.get_json()
    hostname = data.get('hostname')
    ip = data.get('ip')
    as_ip = data.get('as_ip')
    as_port = int(data.get('as_port'))
    logging.info("registeration request received: {}, {}, {}, {}".format(hostname, ip, as_ip, as_port))

    if hostname and ip and as_ip and as_port:
        client_socket = socket(AF_INET, SOCK_RAW)
        msg = "TYPE=A\nNAME={}\nVALUE={}\nTTL=10".format(hostname, ip)
        client_socket.sendto(msg.encode(), (as_ip, as_port))
        modified_message, server_address = client_socket.recvfrom(2048)
        logging.info(modified_message.decode())
        client_socket.close()
        if modified_message.decode() == 'Success':
            return jsonify('Success'), 201
        else:
            return jsonify('Failed'), 500
    else:
        return jsonify('Parameters are not given'), 400

app.run(host='0.0.0.0', port=9090, debug=True)