#!/usr/bin/python3


import webapp


def decorateHTML (text):
    #Produce una salida HTML para un texto de entrada

    return ("<html><h1>" + text + "</h1></html>")

def makeURL(cuerpo, prefix):
    #Devuelve la URL con el prefijo añadido
    URL = cuerpo.split('=')[1]
    if not URL.startswith(prefix):
        URL = prefix + URL
    return URL

def checkDicc(URL, index, diccionario):
    """Dada una URL, busca en diccionario.
    Si se encuentra, devuelve su posicion y 'True'. Si no, devuelve index (el maximo) y 'False'
    """
    if URL in diccionario:
        return (diccionario[URL], False)
    return index, True
    #la forma de arriba es mucho mas limpia
    """for (key, value) in enumerate(diccionario.items()):
        if key == URL:
            return (diccionario[key], False)
    return (index, True)"""

def checkInvertDicc(recurso, diccionario):
    """Busca 'recurso' en el diccionario. Si se encuentra, devuelve 'True' y la URL
    Si no, devuelve URL = '' y 'False'
    """
    if recurso in diccionario:
        return(diccionario[recurso], True)
    return('', False)


class Server(webapp.webApp):


    normalDicc = {'http:google.es': 1} #key--> URL, value--> short url
    invertDicc = {} #key--> short url, value--> URL

    prefix = 'https://' #añadir en las url's sin esto al principio

    formulario = "<form method= POST> Escribe tu URL: <input type='text' name='URL'>"
    formulario = formulario +"<input type=submit value='Pulsame, por Dios' style='height:50px; width:125px'></form> "

    redireccion1 = ("<!DOCTYPE html>\r\n<html>\r\n<head>\r\n"+
                    "<meta http-equiv='Refresh' content='1;url=")
    redireccion2 = "'><body><h2>Redireccionandote...no te muevas!</h></body></html>"

    #Ficheros
    try:
        fichID_1 = open('diccionarioDir', 'r+') #si no existe, se crea
    except FileNotFoundError:
        print('Fichero de inicio 1 no existe...creando')
        fichID_1 = open('diccionarioDir', 'a+')
    try:
        fichID_2 = open('diccionarioIndir', 'r+') #si no existe, se crea
    except FileNotFoundError:
        print('Fichero de inicio 2 no existe...creando')
        fichID_2 = open('diccionarioIndir', 'a+')
    fichID_2.write("hola\n")


    index = 0
    #defino los métodos especiales. El __init__ no hace falta porque se hereda
    def parse(self, request):
        """
        Procesa una petición HTTP y devuelve el ḿetodo asocciado {GET, POST} y el
        Trocea la peticion
        """
        try:
            verb = request.split(' ',1)[0] #metodo
            recurso = request.split()[1][1:] #url pedida
            cuerpo = request.split('\r\n\r\n', 1)[1] #si lo hay, será la url del formulario
        except IndexError:
            print('error en parse')
            return ('')
        #Devuelves los 3 parametros en forma de lista
        return (verb, recurso, cuerpo)


    def process(self, peticion):
        verb = peticion[0];recurso = peticion[1]; cuerpo = peticion[2]
        if verb == 'GET':
            if recurso =='':
                codigo = '200 Ok'
                respuesta = decorateHTML('Bienvenido al mundo del acortamiento <br>\r\n')
                respuesta = respuesta + self.formulario
            else:
                codigo = '200 Ok'
                respuesta = decorateHTML('Eres GET. Te redirijo')
                try:
                    recurso = int(recurso)
                except ValueError:
                    respuesta = decorateHTML('400 Bad Request')
                    respuesta = respuesta+"<p> Recurso no valido. </p>"
                    codigo = '400 Bad Request'
                    return(codigo, respuesta)
                [URL, IsRegistered] = checkInvertDicc(recurso, self.invertDicc)
                if IsRegistered:
                        codigo = '301 Moved Permanently'
                        respuesta = self.redireccion1 + URL+ self.redireccion2
                else:
                        codigo = '400 Bad Request'
                        respuesta = decorateHTML(codigo)+ "<p> Recurso no alojado en el servidor</p>"
        elif verb=='POST':
            if cuerpo == '':
                print('No me han mandado URL')
                respuesta = decorateHTML('No hay URL!')
                codigo = '200 Ok'
            else:
                URL = makeURL(cuerpo, self.prefix)
                print(URL)
                respuesta = decorateHTML('Traduccion realizada con exito.')+"<p>Tus resultados:</p>"
                codigo = '200 Ok'
                [shortURL, IsNew] = checkDicc(URL, self.index, self.normalDicc)
                if IsNew:
                    #lo meto en los diccionarios
                    self.normalDicc[URL]= shortURL
                    self.invertDicc[shortURL]= URL
                    self.index = self.index+1;
                #Genero la respuesta
                urlcorta = self.normalDicc[URL]
                respuesa = decorateHTML('URL acortada con exito')
                respuesta = (respuesta+ "<p>URL corta: </p><a href='"+str(urlcorta)+"'>"+ str(urlcorta)+
                            "</a></p><br>\r\n")
                respuesta = (respuesta + "<p>URL Larga: </p><a href='"+str(URL)+"'>"+str(URL)+
                        "</a></p><br>\r\n")

        else:
            respuesta = '400 Bad Request'
            respuesta = decorateHTML('Metodo invalido')
        return (codigo, respuesta)

if __name__ == "__main__":
    MyServer = Server("localhost", 8080)
    fichID_1.close()
    fichID_2.close()
