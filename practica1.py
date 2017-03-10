#!/usr/bin/python3


import webapp
""" Defino variables que usaré en el resto del programa. Como los diccionarios, indices, formulario..."""


def decorateHTML (text):
    #Produce una salida HTML para un texto de entrada

    return ("<html><body><h1>" + text + "</h1></body></html>")

def makeURL(URL, prefix):
    #Devuelve la URL con el prefijo añadido
    if not URL.startswith(prefix):
        URL = prefix + URL
    return URL

def checkDicc(URL, index):

    for count, item in normalDicc.keys():
        if item == URL: #url ya ha sido acortada
            return (count, False)
    return index, True




class Server(webapp.webApp):


    normalDicc = {'rr':'s'} #key--> URL, value--> short url
    invertDicc = {} #key--> short url, value--> URL

    prefix = 'https://' #añadir en las url's sin esto al principio

    formulario = "<form method= POST> Escribe tu URL: <input type='text' name='URL'>"
    formulario = formulario +"<input type=submit value='Pulsame, por Dios' style='height:50px; width:125px'></form> "

    index = 0
    #defino los métodos especiales. El __init__ no hace falta porque se hereda
    def parse(self, request):
        """
        Procesa una petición HTTP y devuelve el ḿetodo asocciado {GET, POST} y el
        Trocea la peticion
        """
        verb = request.split(' ',1)[0]
        recurso = request.split()[1][1:]
        cuerpo = request.split('\r\n\r\n')[1]
        print(cuerpo)
        return (verb, recurso, cuerpo)


    def process(self, verb, recurso):
        if verb == 'GET':
            if recurso =='':
                codigo = '200 Ok'
                respuesta = decorateHTML('Bienvenido al mundo del acortamiento<br>\r\n')
                respuesta = respuesta + self.formulario
            else:
                codigo = '200 Ok'
                respuesta = decorateHTML('Eres GET. Te redirijo')
        elif verb=='POST':
            if recurso == '':
                print('No me han mandado URL')
                respuesta = decorateHTML('No hay URL!')
                codigo = '200 Ok'
            else:
                URL = makeURL(recurso, self.prefix)
                respuesta = decorateHTML(URL)+decorateHTML('Eres post, recojo tu info y la guardo')
                codigo = '200 Ok'
                [shortURL, IsNew] = checkDicc(URL, self.index)
                if IsNew:
                    self.index = self.index+1;
                print(shortURL, isNew)
        else:
            respuesta = '400 Bad Request'
            respuesta = decorateHTML('Metodo invalido')
        return (codigo, respuesta)

if __name__ == "__main__":
    MyServer = Server("localhost", 8080)
