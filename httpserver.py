#Create http server
import sys
from email.policy import HTTP
from http.server import BaseHTTPRequestHandler, HTTPServer

HOST_NAME = "localhost"
PORT = 8000

# def create_server(host, port):
#     #Create a TCP socket
#     serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     #Bind the socket to address
#     serversocket.bind((host, port))
#     #Listen for incoming connections
#     serversocket.listen(5)
#     return serversocket

class myserver(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.response = '<html><body><h1>Gerardo el que pregunta</h1></body></html>'
        self.send_response(200, "OK")
        self.end_headers()
        self.wfile.write(bytes("<html><body><h1>Gerardo el que pregunta</h1></body></html>", "utf-8"))
        return
    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        print(post_data)
        return
    
def runserver(serverclass=HTTPServer, handlerclass=myserver, server_address=('', 8000)):
    httpd = serverclass(server_address, handlerclass)
    httpd.serve_forever()

if __name__ == '__main__':
    server = HTTPServer((HOST_NAME, PORT), myserver)
    print(f"Server started http://{HOST_NAME}:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
        print("Server stopped successfully")
        sys.exit(0)