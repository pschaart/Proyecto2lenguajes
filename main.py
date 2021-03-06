import os
import time
from graphviz import Digraph
from tkinter import *
from tkinter.filedialog import askopenfilename
import subprocess

#------------Clases----------------
class Gramatica():
    def __init__(self, Nombre, NTerminal, Terminal, Inicial):
        self.Nombre = Nombre
        self.NTerminal = NTerminal
        self.Terminal = Terminal
        self.Inicial = Inicial
        self.Producciones = []

    def InsertarProduc(self, Noterminal, terminal):
        if len(self.Producciones) == 0:
            produccion = []
            produccion.append(Noterminal)
            if len(terminal) > 1:
                terminal = terminal.split(' ')
                for s in terminal:
                    produccion.append(s)
            else:
                produccion.append(terminal)
            self.Producciones.append(produccion)
        else:
            ingresada = False
            for i in self.Producciones:
                if i[0] == Noterminal:
                    i.append('|')
                    if len(terminal) > 1:
                        terminal = terminal.split(' ')
                        for s in terminal:
                            i.append(s)
                    else:
                        i.append(terminal)
                    ingresada = True
            if ingresada == False:
                produccion = []
                produccion.append(Noterminal)
                if len(terminal) > 1:
                    terminal = terminal.split(' ')
                    for x in terminal:
                        produccion.append(x)
                else:
                    produccion.append(terminal)
                self.Producciones.append(produccion)

class ADP():
    def __init__(self,Nombre,Gramatica):
        self.Gramatica = Gramatica
        self.Nombre = Nombre
        self.Estadoi = 'λ,λ,#'
        self.Estadop = ''
        self.Estadoqar = []
        self.Estadoqab = []
        self.Estadof = 'λ,#,λ'



#-----------Memoria----------------
Gramaticas = []
ADPES = []
#-----------Funciones--------------

def MostrarGramaticas():
    try:
        enmenu = False
        while enmenu != True:
            numeroSalida = 0
            print('-------Gramaticas---------')
            for i in range(len(Gramaticas)):
                numeroSalida = i+2
                print(str(i + 1) + '.' + Gramaticas[i].Nombre)
            print(str(numeroSalida) + '.Salir')
            elegida = input()
            #print(elegida)
            if int(elegida) == int(numeroSalida):
                enmenu = True
            else:
                print('Nombre de la gramatica tipo 2: ' + Gramaticas[int(int(elegida) - 1)].Nombre)
                print('No terminales = {' + Gramaticas[int(int(elegida) - 1)].NTerminal + '}')
                print('Terminales = {' + Gramaticas[int(int(elegida) - 1)].Terminal + '}')
                print('No terminal inicial = ' + Gramaticas[int(int(elegida) - 1)].Inicial)
                print('Producciones:')
                for h in Gramaticas[int(elegida) - 1].Producciones:
                    print(h[0] + '->', end='')
                    for j in range(1, len(h)):
                        print(h[j] + ' ', end='')
                    print('')
                os.system("pause")
                os.system("cls")
    except:
        #raise Exception()
        print('Porfavor elija una opcion de la lista')

def Leer(path):
    try:
        documento = open(path,'r')
        GramaticaSL = documento.read().split('*')
        for i in GramaticaSL:
            Guardar = False
            if i == '':
                continue
            else:
                i = i.split('\n')
                i = '%'.join(i)
                i = i.strip('%')
                i = i.split('%')
                Nombre = i[0]
                NTerminales = i[1].split(';')[0]
                Terminales = i[1].split(';')[1]
                Inicial = i[1].split(';')[2]
                GR = Gramatica(Nombre,NTerminales,Terminales,Inicial)
                for j in range(2,len(i)):
                    i[j] = i[j].split('->')
                    veri = i[j][1].split(' ')
                    if len(veri) > 2:
                        Guardar = True
                    GR.InsertarProduc(i[j][0],i[j][1])
                if Guardar == True:
                    Gramaticas.append(GR)
                else:
                    print('No se Guardo la gramatica: ' + Nombre + ' Ya que no es libre del contexto')
        print('Cargado con exito')
        print('-------Gramaticas cargadas---------')
        for i in range(len(Gramaticas)):
            print(str(i + 1) + '.' + Gramaticas[i].Nombre)
    except FileNotFoundError:
        print('Porfavor seleccione un archivo')
    except:
        print('Ha ocurrido un error')

def GenerarAutomata():
    try:
        s = open('Gramatica.html', 'w')
        mensaje = []
        mensaje.append('<html>'
                       '<head></head>')
        for i in range(len(Gramaticas)):
            print(str(i + 1) + '.' + Gramaticas[i].Nombre)
        print('seleccione una gramatica:')
        gramausar = Gramaticas[int(input()) - 1]
        ADPMOMEN = ADP('AP_' + gramausar.Nombre,gramausar)
        f = Digraph('Automata de pila', filename='AP_' + gramausar.Nombre + '.gv', format='jpg')
        f.attr(rankdir= 'LR')
        f.attr('node', shape='circle')
        f.node('i')
        f.node('p')
        f.node('q')

        f.edge('i','p',label='λ,λ;#')
        f.edge('p', 'q', label=('λ,λ;' + gramausar.Inicial))
        ADPMOMEN.Estadop = gramausar.Inicial
        for m in gramausar.Producciones:
            if '|' in m:
                sinm=[]
                for k in range(1, len(m)):
                    sinm.append(m[k])
                sinm = ' '.join(sinm)
                sinm = sinm.split('|')
                for l in sinm:
                    texto = []
                    texto.append('λ,')
                    texto.append(m[0] + ';')
                    texto.append(l)
                    texto = ''.join(texto)
                    ADPMOMEN.Estadoqar.append(texto)
            else:
                texto = []
                texto.append('λ,')
                texto.append(m[0] + ';')
                for i in range(1,len(m)):
                    texto.append(m[i])
                texto = ''.join(texto)
                ADPMOMEN.Estadoqar.append(texto)
        termin = gramausar.Terminal
        termin = termin.split(',')
        for h in termin:
            texto = []
            texto.append(h + ',')
            texto.append(h + ';λ')
            texto = ''.join(texto)
            ADPMOMEN.Estadoqab.append(texto)
        arriba = []
        for j in ADPMOMEN.Estadoqar:
            arriba.append(j)
        arriba = '\\n'.join(arriba)
        abajo = []
        for j in ADPMOMEN.Estadoqab:
            abajo.append(j)
        abajo = '\\n'.join(abajo)
        f.edge('q:n', 'q:n', label=(arriba))
        f.edge('q:s', 'q:s', label=(abajo))
        f.attr('node', shape='doublecircle')
        f.node('f')
        f.edge('q','f',label=('λ,#,λ'))

        f.render()
        Guardar = True
        for i in ADPES:
            if i.Nombre == 'AP_' + gramausar.Nombre:
                Guardar = False
                print('no se guardo porque ya existe')
        if Guardar:
            ADPES.append(ADPMOMEN)
        mensaje.append('<p>')
        mensaje.append('Nombre de la gramatica tipo 2: ' + gramausar.Nombre + '<br>')
        mensaje.append('No terminales = {' + gramausar.NTerminal + '}<br>')
        mensaje.append('Terminales = {' + gramausar.Terminal + '}<br>')
        mensaje.append('No terminal inicial = ' + gramausar.Inicial + '<br>')
        mensaje.append('Producciones:<br>')
        for h in gramausar.Producciones:
            mensaje.append(h[0] + '->')
            for j in range(1, len(h)):
                mensaje.append(h[j] + ' ')
            mensaje.append('<br>')
        mensaje.append('<p>')
        mensaje.append('<img src="AP_' + gramausar.Nombre + '.gv.jpg">')
        mensaje.append('</html>')
        mensaje = ''.join(mensaje)
        s.write(mensaje)
        s.close()
        subprocess.Popen(['Gramatica.html'], shell=True)
    except:
        #raise Exception()
        print('Ha ocurrido un error')

def AnalizarCadenaG():
    try:
        f = open('archivo.html', 'w')
        mensaje = []
        mensaje.append('<html>'
                       '<head></head>'
                       '<table border="1">')
        pila = []
        for i in range(len(ADPES)):
            print(str(i + 1) + '.' + ADPES[i].Nombre)
        print('seleccione una Automata de pila:')
        ADPusar = ADPES[int(input()) - 1]
        print('ingrese una cadena')
        cadena = input()
        pila.append('#')
        mensaje.append('<div style="border: 1px solid blue;">'
                        '<img src="' + ADPusar.Nombre + '.gv.jpg">'
                        '<table border="1">' 
                        '<tr>'
                        '<td>Pila</td>' 
                        '<td>' + ''.join(pila) + '</td>'
                        '</tr>'
                        '<tr>'
                        '<td>Cadena</td>' 
                        '<td>' + cadena + '</td>'
                        '</tr>'
                        '</table>'
                        '</div>')
        inicial = ADPusar.Estadop
        pila.append(inicial)
        while cadena != '' or len(pila) != 1 :
            print(pila)
            ingresada = False
            ultimo = pila[len(pila)-1]
            transis = 0
            for i in ADPusar.Estadoqar:
                transi1 = i.split(';')
                transi2 = transi1[0].split(',')
                if transi2[1] == ultimo:
                    transis += 1
            for i in ADPusar.Estadoqar:
                transi1 = i.split(';')
                transi1[1] = ''.join(transi1[1].split(' '))
                transi2 = transi1[0].split(',')
                if transis == 1:
                    pila.pop()
                    num = len(transi1[1]) - 1
                    for k in transi1[1]:
                        pila.append(transi1[1][num])
                        num -= 1
                    ingresada = True
                    mensaje.append('<div style="border: 1px solid blue;">'
                                   '<img src="' + ADPusar.Nombre + '.gv.jpg">'
                                                                   '<table border="1">'
                                                                   '<tr>'
                                                                   '<td>Pila</td>'
                                                                   '<td>' + ''.join(pila) + '</td>'
                                                                                            '</tr>'
                                                                                            '<tr>'
                                                                                            '<td>Cadena</td>'
                                                                                            '<td>' + cadena + '</td>'
                                                                                                              '</tr>'
                                                                                                              '</table>'
                                                                                                              '</div>')
                    break

                elif transi2[1] == ultimo:
                    if len(transi1[1]) > 1 and cadena[0] in transi1[1]:
                        pila.pop()
                        num = len(transi1[1]) - 1
                        for k in transi1[1]:
                            pila.append(transi1[1][num])
                            num -= 1
                        ingresada = True
                        mensaje.append('<div style="border: 1px solid blue;">'
                                       '<img src="' + ADPusar.Nombre + '.gv.jpg">'
                                                                       '<table border="1">'
                                                                       '<tr>'
                                                                       '<td>Pila</td>'
                                                                       '<td>' + ''.join(pila) + '</td>'
                                                                                                '</tr>'
                                                                                                '<tr>'
                                                                                                '<td>Cadena</td>'
                                                                                                '<td>' + cadena + '</td>'
                                                                                                                  '</tr>'
                                                                                                                  '</table>'
                                                                                                                  '</div>')
                        break
                    elif cadena[0] in transi1[1]:
                        pila.pop()
                        num = len(transi1[1]) - 1
                        for k in transi1[1]:
                            pila.append(transi1[1][num])
                            num -= 1
                        ingresada = True
                        mensaje.append('<div style="border: 1px solid blue;">'
                                       '<img src="' + ADPusar.Nombre + '.gv.jpg">'
                                                                       '<table border="1">'
                                                                       '<tr>'
                                                                       '<td>Pila</td>'
                                                                       '<td>' + ''.join(pila) + '</td>'
                                                                                                '</tr>'
                                                                                                '<tr>'
                                                                                                '<td>Cadena</td>'
                                                                                                '<td>' + cadena + '</td>'
                                                                                                                  '</tr>'
                                                                                                                  '</table>'
                                                                                                                  '</div>')
                        break
            if ingresada == False:
                for i in ADPusar.Estadoqar:
                    transi1 = i.split(';')
                    transi1[1] = ''.join(transi1[1].split(' '))
                    transi2 = transi1[0].split(',')
                    if (transi2[1] == ultimo) and (len(transi1[1]) == 1):
                        pila.pop()
                        num = len(transi1[1]) - 1
                        for k in transi1[1]:
                            pila.append(transi1[1][num])
                            num -= 1
                        ingresada = True
                        mensaje.append('<div style="border: 1px solid blue;">'
                                       '<img src="' + ADPusar.Nombre + '.gv.jpg">'
                                                                       '<table border="1">'
                                                                       '<tr>'
                                                                       '<td>Pila</td>'
                                                                       '<td>' + ''.join(pila) + '</td>'
                                                                                                '</tr>'
                                                                                                '<tr>'
                                                                                                '<td>Cadena</td>'
                                                                                                '<td>' + cadena + '</td>'
                                                                                                                  '</tr>'
                                                                                                                  '</table>'
                                                                                                                  '</div>')
                        break
            if ingresada == False:
                for i in ADPusar.Estadoqab:
                    transi1 = i.split(';')
                    transi2 = transi1[0].split(',')
                    if transi2[0] == ultimo:
                        cadena = cadena.lstrip(ultimo)
                        pila.pop()
                        ingresada = True
                        mensaje.append('<div style="border: 1px solid blue;">'
                                       '<img src="' + ADPusar.Nombre + '.gv.jpg">'
                                                                       '<table border="1">'
                                                                       '<tr>'
                                                                       '<td>Pila</td>'
                                                                       '<td>' + ''.join(pila) + '</td>'
                                                                                                '</tr>'
                                                                                                '<tr>'
                                                                                                '<td>Cadena</td>'
                                                                                                '<td>' + cadena + '</td>'
                                                                                                                  '</tr>'
                                                                                                                  '</table>'
                                                                                                                  '</div>')
                        break
            if ingresada == False:
                mensaje.append('<div style="border: 1px solid blue;">'
                               '<img src="' + ADPusar.Nombre + '.gv.jpg">'
                                                               '<table border="1">'
                                                               '<tr>'
                                                               '<td>Pila</td>'
                                                               '<td>' + ''.join(pila) + '</td>'
                                                                                        '</tr>'
                                                                                        '<tr>'
                                                                                        '<td>Cadena</td>'
                                                                                        '<td>' + cadena + '</td>'
                                                                                                          '</tr>'
                                                                                                          '</table>'
                                                                                                          '</div>'
                                                                                                          'cadena rechazada')
                print('Cadena rechazada')
                mensaje.append('</html>')
                mensaje = ''.join(mensaje)
                f.write(mensaje)
                f.close()
                subprocess.Popen(['archivo.html'], shell=True)
                break
        print(pila)
        if len(cadena) > 1:
            return
        else:
            pila.pop()
            mensaje.append('<div style="color: blue;">'
                           '<img src="' + ADPusar.Nombre + '.gv.jpg">'
                                                           '<table border="1">'
                                                           '<tr>'
                                                           '<td>Pila</td>'
                                                           '<td>' + ''.join(pila) + '</td>'
                                                                                    '</tr>'
                                                                                    '<tr>'
                                                                                    '<td>Cadena</td>'
                                                                                    '<td>' + cadena + '</td>'
                                                                                                      '</tr>'
                                                                                                      '</table>'
                                                                                                      '</div>'
                                                                                                      'Cadena aceptada')
        mensaje.append('</html>')
        mensaje = ''.join(mensaje)
        f.write(mensaje)
        f.close()
        subprocess.Popen(['archivo.html'], shell=True)
    except:
        print('Ha ocurrido un error')

def AnalizarCadenaT():
    try:
        f = open('archivoT.html', 'w')
        iteracion = 0
        mensaje = []
        mensaje.append('<html>'
                       '<head></head>')
        mensaje.append(
            '<table border="1">'
            '<tr>'
            '<td>iteracion</td>'
            '<td>pila</td>'
            '<td>entrada</td>'
            '<td>transiciones</td>'
            '</tr>')
        pila = []
        for i in range(len(ADPES)):
            print(str(i + 1) + '.' + ADPES[i].Nombre)
        print('seleccione una Automata de pila:')
        ADPusar = ADPES[int(input()) - 1]
        print('ingrese una cadena')
        cadena = input()
        pila.append('#')
        iteracion += 1
        mensaje.append(
            '<tr>'
            '<td>' + str(iteracion) + '</td>'
            '<td>' + ''.join(pila) + '</td>'
            '<td>' + cadena + '</td>'
            '<td>(i, $, $;p,#)</td>'
            '</tr>')
        inicial = ADPusar.Estadop
        pila.append(inicial)
        iteracion += 1
        mensaje.append(
            '<tr>'
            '<td>' + str(iteracion) + '</td>'
            '<td>' + ''.join(pila) + '</td>'
            '<td>' + cadena + '</td>'
            '<td>(p, $, $;q,'+ inicial +')</td>'
            '</tr>')
        while cadena != '' or len(pila) != 1 :
            iteracion += 1
            print(pila)
            ingresada = False
            ultimo = pila[len(pila)-1]
            transis = 0
            for i in ADPusar.Estadoqar:
                transi1 = i.split(';')
                transi2 = transi1[0].split(',')
                if transi2[1] == ultimo:
                    transis += 1
            for i in ADPusar.Estadoqar:
                transi1 = i.split(';')
                transi1[1] = ''.join(transi1[1].split(' '))
                transi2 = transi1[0].split(',')
                if transis == 1:
                    pila.pop()
                    num = len(transi1[1]) - 1
                    for k in transi1[1]:
                        pila.append(transi1[1][num])
                        num -= 1
                    ingresada = True
                    mensaje.append(
                        '<tr>'
                        '<td>' + str(iteracion) + '</td>'
                        '<td>' + ''.join(pila) + '</td>'
                        '<td>' + cadena + '</td>'
                        '<td>(q,$,'+ transi2[1]+';q,'+ ultimo +')</td>'
                        '</tr>')
                    break

                elif transi2[1] == ultimo:
                    if len(transi1[1]) > 1 and cadena[0] in transi1[1]:
                        pila.pop()
                        num = len(transi1[1]) - 1
                        for k in transi1[1]:
                            pila.append(transi1[1][num])
                            num -= 1
                        ingresada = True
                        mensaje.append(
                            '<tr>'
                            '<td>' + str(iteracion) + '</td>'
                            '<td>' + ''.join(pila) + '</td>'
                            '<td>' + cadena + '</td>'
                            '<td>(q,$,'+ transi2[1]+';q,'+ ultimo +')</td>'
                            '</tr>')
                        break
                    elif cadena[0] in transi1[1]:
                        pila.pop()
                        num = len(transi1[1]) - 1
                        for k in transi1[1]:
                            pila.append(transi1[1][num])
                            num -= 1
                        ingresada = True
                        mensaje.append(
                            '<tr>'
                            '<td>' + str(iteracion) + '</td>'
                            '<td>' + ''.join(pila) + '</td>'
                            '<td>' + cadena + '</td>'
                            '<td>(q,$,'+ transi2[1]+';q,'+ ultimo +')</td>'
                            '</tr>')
                        break
            if ingresada == False:
                for i in ADPusar.Estadoqar:
                    transi1 = i.split(';')
                    transi1[1] = ''.join(transi1[1].split(' '))
                    transi2 = transi1[0].split(',')
                    if (transi2[1] == ultimo) and (len(transi1[1]) == 1):
                        pila.pop()
                        num = len(transi1[1]) - 1
                        for k in transi1[1]:
                            pila.append(transi1[1][num])
                            num -= 1
                        ingresada = True
                        mensaje.append(
                            '<tr>'
                            '<td>' + str(iteracion) + '</td>'
                            '<td>' + ''.join(pila) + '</td>'
                            '<td>' + cadena + '</td>'
                            '<td>(q,$,'+ transi2[1]+';q,'+ ultimo +')</td>'
                            '</tr>')
                        break
            if ingresada == False:
                for i in ADPusar.Estadoqab:
                    transi1 = i.split(';')
                    transi2 = transi1[0].split(',')
                    if transi2[0] == ultimo:
                        cadena = cadena.lstrip(ultimo)
                        pila.pop()
                        ingresada = True
                        mensaje.append(
                            '<tr>'
                            '<td>' + str(iteracion) + '</td>'
                            '<td>' + ''.join(pila) + '</td>'
                            '<td>' + cadena + '</td>'
                            '<td>(q,' + transi1[0] + ';q,' + ultimo + ')</td>'
                            '</tr>')
                        break
            if ingresada == False:
                mensaje.append(
                    '<tr>'
                    '<td>' + str(iteracion) + '</td>'
                    '<td>' + ''.join(pila) + '</td>'
                    '<td>' + cadena + '</td>'
                    '<td> vacio </td>'
                    '</tr>'
                    '</table>'
                    'Cadena rechazada')
                print('Cadena rechazada')
                mensaje.append('</html>')
                mensaje = ''.join(mensaje)
                f.write(mensaje)
                f.close()
                subprocess.Popen(['archivo.html'], shell=True)
                break
        print(pila)
        if len(cadena) > 1:
            return
        else:
            pila.pop()
            iteracion += 1
            mensaje.append(
                '<tr>'
                '<td>' + str(iteracion) + '</td>'
                '<td>' + ''.join(pila) + '</td>'
                '<td>' + cadena + '</td>'
                '<td>(q,$,#;f,$)</td>'
                '</tr>')
        mensaje.append('</html>')
        mensaje = ''.join(mensaje)
        f.write(mensaje)
        f.close()
        subprocess.Popen(['archivoT.html'], shell=True)
    except:
        #raise Exception()
        print('Ha ocurrido un error')

#-----------Menu-----------
segundos = 5
print('----------Proyecto 2---------')
print('creado por Pablo Gerardo Schaart Calderon')
print('Carnet: 201800951')
while segundos != 0:
    print(segundos)
    time.sleep(1)
    segundos -= 1
opcion = 0
print('!Bienvenido¡')
try:
    while int(opcion) != 6:
        try:
            print('------------Menu---------------')
            print('1.Cargar el archivo')
            print('2.Mostrar informacion general de la gramatica')
            print('3.Generar automata de pila eqivalente')
            print('4.Reporte de recorrido')
            print('5.Reporte en tabla')
            print('6.Salir')
            opcion = input()
            if int(opcion) == 1:
                root = Tk()
                NombreArchivo = askopenfilename()
                root.withdraw()
                Leer(NombreArchivo)
            elif int(opcion) == 2:
                MostrarGramaticas()
            elif int(opcion) == 3:
                GenerarAutomata()
            elif int(opcion) == 4:
                AnalizarCadenaG()
            elif int(opcion) == 5:
                AnalizarCadenaT()
        except:
            #raise Exception()
            print('ha ocurrido un error... regresando al menu principal')
except:
    #raise Exception()
    print('ha ocurrido un error...')