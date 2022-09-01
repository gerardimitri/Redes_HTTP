import socket
from utils import *
import json

HOST = "example.com"
PORT = 8000

def parseHTTP(data):
    """
    Parses the HTTP request and returns a dictionary with the request's headers and body.
    """
    data = data.split('\r\n\r\n')
    headers = data[0].split('\r\n')
    body = data[1]
    return {'headers': headers, 'body': body}

def buildHTTP(headers, body):
    """
    Builds an HTTP response from the given headers and body.
    """
    return str(headers) + str(body)

def headerToJson(headers):
    """
    Converts the headers of an HTTP request to a JSON object.
    """
    json = {}
    for header in headers:
        header = header.split(': ')
        json[header[0]] = header[1]
    return json

def bodyToJson(body):
    """
    Converts the body of an HTTP request to a JSON object.
    """
    return json.loads(body)
