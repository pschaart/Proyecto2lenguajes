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

#-----------Memoria----------------
Gramaticas = []

#-----------Funciones--------------

def MostrarGramaticas():
    print('-------Gramaticas cargadas---------')
    for i in range(len(Gramaticas)):
        print(str(i+1) + '.' + Gramaticas[i].Nombre)

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
                            produc = []
                            produc.append(i[j][0])
                            for l in k:
                                produc.append(l)
                            GR.Producciones.append(produc)
                    else:
                        i[j][1] = i[j][1].split(' ')
                        if len(i[j][1]) > 2:
                            Guardar = True
                        produc = []
                        produc.append(i[j][0])
                        for s in i[j][1]:
                            produc.append(s)
                        GR.Producciones.append(produc)
                if Guardar == True:
                    Gramaticas.append(GR)
                else:
                    print('No se Guardo la gramatica: ' + Nombre + ' Ya que no es libre del contexto')
        print('Cargado con exito')
        MostrarGramaticas()
    except FileNotFoundError:
        print('Porfavor seleccione un archivo')
    except:
        raise Exception('Ha ocurrido un error')

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
