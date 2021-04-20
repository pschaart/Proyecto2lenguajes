import time
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

    def InsertarProduc(self,Noterminal,terminal):
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
                    for s in terminal:
                        produccion.append(s)
                else:
                    produccion.append(terminal)
                self.Producciones.append(produccion)



#-----------Memoria----------------
Gramaticas = []

#-----------Funciones--------------

def MostrarGramaticas():
    try:
        print('-------Gramaticas---------')
        for i in range(len(Gramaticas)):
            print(str(i + 1) + '.' + Gramaticas[i].Nombre)
        elegida = input()
        print('Nombre de la gramatica tipo 2: ' + Gramaticas[int(int(elegida) - 1)].Nombre)
        print('No terminales = {' + Gramaticas[int(int(elegida) - 1)].NTerminal + '}')
        print('Terminales = {' + Gramaticas[int(int(elegida) - 1)].Terminal + '}')
        print('No terminal inicial = ' + Gramaticas[int(int(elegida) - 1)].Inicial)
        print('Producciones:')
        print(Gramaticas[int(int(elegida) - 1)].Producciones)
        for h in Gramaticas[int(elegida) - 1].Producciones:
            print(h[0] + '->', end='')
            for j in h[1]:
                print(j + ' ', end='')
            print('')

    except:
        raise Exception('Porfavor elija una opcion de la lista')

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
                    if "|" in i[j][1]:
                        i[j][1] = i[j][1].split('|')
                        for k in i[j][1]:
                            k = k.split(' ')
                            if len(k) > 2:
                                Guardar = True
                            GR.InsertarProduc(i[j][0],i[j][1])
                    else:
                        i[j][1] = i[j][1].split(' ')
                        if len(i[j][1]) > 2:
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
        Exception('Ha ocurrido un error')

#-----------Menu-----------
segundos = 5
print('----------Proyecto 2---------')
print('creado por Pablo Gerardo Schaart Calderon')
print('Carnet: 201800951')
#while segundos != 0:
#    print(segundos)
#    time.sleep(1)
#    segundos -= 1
opcion = 0
print('!Bienvenido¡')
while opcion != 6:
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
