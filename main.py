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
    def __init__(self,Nombre):
        self.Nombre = Nombre
        self.Estadoi = 'λ,λ,#'
        self.Estadop = []
        self.Estadoq = []
        self.Estadof = []



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
        for i in range(len(Gramaticas)):
            print(str(i + 1) + '.' + Gramaticas[i].Nombre)
        print('seleccione una gramatica:')
        gramausar = Gramaticas[int(input()) - 1]
        ADPMOMEN = ADP('AP_' + gramausar.Nombre)
        f = Digraph('Automata de pila', filename='AP_.gv', format='png')
        f.attr(rankdir= 'LR')
        f.attr('node', shape='circle')
        f.node('i')
        f.node('p')
        f.node('q')

        f.edge('i','p',label='λ,λ,#')
        f.edge('p', 'q', label=('λ,λ,' + gramausar.Inicial))
        ADPMOMEN.Estadop.append('λ,λ,' + gramausar.Inicial)
        for m in gramausar.Producciones:
            if '|' in m:
                iz = m[0]
                sin0 = m
                sin0.pop(0)
                sin0 = ''.join(sin0)
                sin0 = sin0.split('|')
                print(sin0)
                #ADPMOMEN.Estadoq.append()
        ex = str('prueba\\n'
                 'hola\\n'
                 'adios')
        f.edge('q', 'q', label=(ex))
        f.view()

    except:
        raise Exception()
        print('Ha ocurido un error')



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
    elif int(opcion) == 3:
        GenerarAutomata()

