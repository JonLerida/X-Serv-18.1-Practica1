#!/usr/bin/python3

"""
webApp class
 Root for hierarchy of classes implementing web applications

 Copyright Jesus M. Gonzalez-Barahona and Gregorio Robles (2009-2015)
 jgb @ gsyc.es
 TSAI, SAT and SARO subjects (Universidad Rey Juan Carlos)
 October 2009 - February 2015
"""

import socket



def decorateHTML (text):

    return ("<html><body>" + text + "</body></html>")

class webApp:
    """Root of a hierarchy of classes implementing web applications

    This class does almost nothing. Usually, new classes will
    inherit from it, and by redefining "parse" and "process" methods
    will implement the logic of a web application in particular.
    """

    def parse(self, request):
        """Parse the received request, extracting the relevant information."""

        return None

    def process(self, verb, parsedRequest):
        """Process the relevant elements of the request.

        Returns the HTTP code for the reply, and an HTML page.
        """

        """
        Si el método es GET, diferenciar si es barra
        """

        if verb == 'GET':
            print(parsedRequest)
            if parsedRequest == '':
                print('es get y barra')
                respuesta = "<html><body><h1>Bienvenido a la Practica1 de Jon Lerida, bro</h1><br>\r\n"
                respuesta = respuesta +("<form action=''>\r\n"+
                                        "URL original:<br>\r\n"+
                                        "<input type='text' name 'url'>"+
                                        "<br>\r\n"+
                                        "</form></body></html>")

            else:
                print('Es get y no barra')
                respuesta = decorateHTML('No me has pedido barra, redirigiendo a la url pedida')

            return ("200 OK", respuesta)
        elif verb == 'POST':
            print('Me ha llegado un POST')
        else:
            print('Me ha llegado algo que no es get')
            respuesta = decorateHTML('Metodo invalido')
            return ("404 Not Found", respuesta)


    def __init__(self, hostname, port):
        """Initialize the web application."""

        # Create a TCP objet socket and bind it to a port
        mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        mySocket.bind((hostname, port))

        # Queue a maximum of 5 TCP connection requests
        mySocket.listen(5)

        # Accept connections, read incoming data, and call
        # parse and process methods (in a loop)
        try:
            while True:
                print ('Waiting for connections')
                (recvSocket, address) = mySocket.accept()
                print ('HTTP request received (going to parse and process):')
                request = recvSocket.recv(2048).decode('utf-8')
                print (request)
                [verb, recurso] = self.parse(request)
                (returnCode, htmlAnswer) = self.process(verb, recurso)
                print ('Answering back...')
                recvSocket.send(bytes("HTTP/1.1 " + returnCode + " \r\n\r\n"
                                + htmlAnswer + "\r\n", 'utf-8'))
                recvSocket.close()
        except KeyboardInterrupt:
            mySocket.close()
            print('\n\nClosing...')

if __name__ == "__main__":
    NormalDicc = {} #Key --> URL; Value --> Index
    InvertDicc = {} #Key --> index; Value--> URL
    testWebApp = webApp("localhost", 8080)
