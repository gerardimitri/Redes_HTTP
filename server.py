# -*- coding: utf-8 -*-
import socket
from proxy import *
import json

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

HOST = "localhost" #"example.com"
PORT = 8000

file_path = "config.json"
with open(file_path) as j:
     data_json = json.load(j)

for key in data_json:
    HTTP_RESPONSE_HEAD += f"{key}: {data_json[key]}\r\n"

# definimos el tamaño del buffer de recepción ¿Cómo se ven los trozos de mensaje recibidos si usamos 'buff_size = 2' ?
buff_size = 4096
address = (HOST, PORT)

print('Creando socket - Servidor')
# armamos el socket
# los parámetros que recibe el socket indican el tipo de conexión
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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

    # luego recibimos el mensaje usando la función que programamos
    received_message = connection_socket.recv(buff_size).decode()
    received_message_headers = parseHTTP(received_message).get('headers')

    print(' -> Se ha recibido el siguiente mensaje: {}'.format(received_message))

    # respondemos
    response_message = buildHTTP(HTTP_RESPONSE_HEAD, HTTP_RESPONSE_BODY).encode()
    connection_socket.send(response_message)


    # cerramos la conexión
    # notar que la dirección que se imprime indica un número de puerto distinto al 8888
    connection_socket.close()
    print("conexión con {} ha sido cerrada".format(address))

    # seguimos esperando por si llegan otras conexiones
