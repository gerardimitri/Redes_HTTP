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
    headers = data[0]
    body = data[1]
    return {'headers': headers, 'body': body}


def buildHTTP(headers, body):
    """
    Builds an HTTP response from the given headers and body.
    """
    return str(headers) + "\r\n" + str(body)

def getUri(headers):
    """
    Returns the URI of the HTTP request.
    """
    headers = headers.split('\r\n')
    return headers[0].split(' ')[1]

def headerToJson(headers):
    """
    Converts the headers of an HTTP request to a JSON object.
    """
    headers = headers.split('\r\n')
    json = {}
    headers = headers[1:]
    for header in headers:
        header = header.split(': ')
        json[header[0]] = header[1]
    return json

def bodyToJson(body):
    """
    Converts the body of an HTTP request to a JSON object.
    """
    return json.loads(body)

def replaceForbiddenWords(aString, ListOfDictsOfForbiddenWords):
    """
    Replaces forbidden words in a string with asterisks.
    """
    for dict in ListOfDictsOfForbiddenWords:
        for key in dict:
            aString = aString.replace(key, dict[key])
    return aString