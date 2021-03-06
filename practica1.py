#!/usr/bin/python3
# -*- coding: utf-8 -*


import webapp
import csv


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
    # ESTO SE EJECUTA AL PRINCIPIO
    # Diccionarios de URLs
    normalDicc = {} #key--> URL, value--> short url
    invertDicc = {} #key--> short url, value--> URL

    prefix = 'https://' #añadir en las url's sin esto al principio

    formulario = "<form method= POST> Escribe tu URL: <input type='text' name='URL'>"
    formulario = formulario +"<input type=submit value='Pulsame, por Dios' style='height:50px; width:125px'></form> "

    redireccion1 = ("<!DOCTYPE html>\r\n<html>\r\n<head>\r\n"+
                    "<meta http-equiv='Refresh' content='1;url=")
    redireccion2 = "'><body><h2>Redireccionandote...no te muevas!</h></body></html>"

    index = 0 #Primera URL acortada, empieza en 0

    # Abrimos el fichero en csv para recoger las posibles direcciones guardadas y las metemos en los diccionarios
    # line es una lista con todos los elementos de una línea. Me quedo con el primer elemento (la url)
    # Usar with permite no tener que andar cerrando los ficheros
    with open('diccionarioDir.csv', 'r+') as dicc_directo:
        reader = csv.reader(dicc_directo)
        print("Recuperando diccionarios de URL's validas...")
        for line in reader:
            normalDicc[line[0]] = index
            invertDicc[index] = line[0]
            index = index+1





    #defino los métodos especiales. Deben tener los mismo argumentos que los de la clase que hereda (webapp)
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
            if cuerpo == 'URL=':
                print('No me han mandado URL')
                respuesta = decorateHTML('La caja esta para escribir')
                codigo = '200 Ok'
            else:
                URL = makeURL(cuerpo, self.prefix)
                print('--------------')
                print('URL procesada...')
                respuesta = decorateHTML('Traduccion realizada con exito.')+"<p>Tus resultados:</p>"
                codigo = '200 Ok'
                [shortURL, IsNew] = checkDicc(URL, self.index, self.normalDicc)
                if IsNew:
                    #lo meto en los diccionarios
                    self.normalDicc[URL]= shortURL
                    self.invertDicc[shortURL]= URL

                    #actualizo el fichero CSV para futuras peticiones
                    with open('diccionarioDir.csv', 'a') as dicc1:
                            writer1 = csv.writer(dicc1)
                            writer1.writerow([URL])
                    #Actualizamos el Index
                    self.index = self.index+1;

                #Genero la respuesta (busco en el diccionario la URL corta)
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
