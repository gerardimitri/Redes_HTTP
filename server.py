# -*- coding: utf-8 -*-
import socket
from proxy import *
import json
import utils

HTTP_RESPONSE_BODY = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Hello World</title>
</head>
<body>
    <h1>Hello World</h1>
</body>
</html>
'''

HTTP_RESPONSE_HEAD = f'''HTTP/1.1 200 OK\r\n
Host: example.com\r\n
Content-Type: text/html; charset=UTF-8\r\n
Content-Length: {len(HTTP_RESPONSE_BODY)}\r\n
Connection: close\r\n
'''

HTTP_FORBIDDEN = "HTTP/1.1 403 FORBIDDEN\r\n\r\n"

HTTP_HEAD_ADDONS = ''

HOST = "localhost" #"example.com"
PORT = 8000
DESTINATION_ADDRESS = ""
DESTINATION_PORT = 5000

file_path = "config.json"
with open(file_path) as j:
     data_json = json.load(j)

for key in data_json:
    HTTP_HEAD_ADDONS += f"{key}: {data_json[key]}\r\n"

blocked = "blocked.json"
with open(blocked) as j:
     blocked_json = json.load(j)

blocked_uris = blocked_json["blocked"]
forbidden_words = blocked_json["forbidden_words"]

# definimos el tamaño del buffer de recepción ¿Cómo se ven los trozos de mensaje recibidos si usamos 'buff_size = 2' ?
buff_size = 4096
address = (HOST, PORT)

#signal.signal(signal.SIGINT, self.shutdown) # Ctrl + C

print('Creando socket - Servidor')
# armamos el socket
# los parámetros que recibe el socket indican el tipo de conexión
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

destination_address = (DESTINATION_ADDRESS, DESTINATION_PORT)

# lo conectamos al server, en este caso espera mensajes localmente en el puerto 8888
server_socket.bind(address)

# hacemos que sea un server socket y le decimos que tenga a lo mas 3 peticiones de conexión encoladas
# si recibiera una 4ta petición de conexión la va a rechazar
server_socket.listen(3)

# nos quedamos esperando, como buen server, a que llegue una petición de conexión
print('... Esperando clientes')
while True:
    # cuando llega una petición de conexión la aceptamos
    # y sacamos los datos de la conexión entrante (nuevo_socket, dirección)
    connection_socket, address = server_socket.accept()
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # luego recibimos el mensaje usando la función que programamos
    received_message = connection_socket.recv(buff_size).decode()
    received_message_headers = parseHTTP(received_message).get('headers')

    print(' -> Mensaje recibido: <<' + received_message + '>>')
    header_json = headerToJson(received_message_headers)
    uri = getUri(received_message_headers)
    print("URI: " + uri)
    client_address = (header_json.get('Host'), 80)
    message = HTTP_FORBIDDEN.encode()

    if uri not in blocked_uris:
        client_socket.connect(client_address)

        print(' -> Se ha recibido el siguiente mensaje: {}'.format(received_message))

        # respondemos
        received_message_headers = received_message_headers + "\r\n" + HTTP_HEAD_ADDONS
        response_message = buildHTTP(received_message_headers, "").encode()
        
        client_socket.send(response_message)
        message = client_socket.recv(buff_size).decode()
        print(" -> Mensaje recibido: " + message)
        message = parseHTTP(message)
        message_headers = message.get('headers')
        header_first_line = getHeaderFirstLine(message_headers) + "\r\n"
        header_json = headerToJson(message_headers)
        message_body = message.get('body')
        message_body = replaceForbiddenWords(message_body, forbidden_words)
        header_json['Content-Length'] = len(message_body + message_headers + "\r\n")
        message_headers = header_first_line + jsonToHeader(header_json)
        message = buildHTTP(message_headers, message_body).encode()
    connection_socket.send(message)
    #print ("Enviamos cositas... \n" + response_message)

    # cerramos la conexión
    # notar que la dirección que se imprime indica un número de puerto distinto al 8888
    connection_socket.close()
    client_socket.close()
    print("conexión con {} ha sido cerrada".format(address))

    break
    # seguimos esperando por si llegan otras conexiones