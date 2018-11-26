from subprocess import Popen, PIPE
from random import randint
import csv
import numpy as np

savePoblacion = []

def mapeo():
    inicio = np.array([1, 2, 3, 4, 5])
    for i in inicio:
        if i == 1:
            inicio[0] = 1
        if i == 2:
            inicio[1] = randint(3, 26)
        if i == 3:
            inicio[2] = randint(500, 1000)
        if i == 4:
            inicio[3] = randint(1, 30)
        if i == 5:
            inicio[4] = randint(1, 20)

    return inicio


def poblacionInicial():
    pobInicial = np.array([[1, 2, 3, 4, 5],[1, 2, 3, 4, 5],[1, 2, 3, 4, 5],[1, 2, 3, 4, 5],[1, 2, 3, 4, 5],[1, 2, 3, 4,5],[1, 2, 3, 4, 5],[1, 2, 3, 4, 5],[1, 2, 3, 4, 5],[1, 2, 3, 4, 5]])
    for i in range(1, 11):
        if i == 1:
            pobInicial[0] = mapeo()
        if i == 2:
            pobInicial[1] = mapeo()
        if i == 3:
            pobInicial[2] = mapeo()
        if i == 4:
            pobInicial[3] = mapeo()
        if i == 5:
            pobInicial[4] = mapeo()
        if i == 6:
            pobInicial[5] = mapeo()
        if i == 7:
            pobInicial[6] = mapeo()
        if i == 8:
            pobInicial[7] = mapeo()
        if i == 9:
            pobInicial[8] = mapeo()
        if i == 10:
            pobInicial[9] = mapeo()

    return pobInicial

def convertirABinario():
    datos = poblacionInicial()
    representacionBinaria = []
    for row in datos:
        capasToBinario = '{0:01b}'.format(int(row[0]))
        neuronasToBinario = '{0:05b}'.format(int(row[1]))
        epocasToBinario = '{0:010b}'.format(int(row[2]))
        learningRateToBinario = '{0:05b}'.format(int(row[3]))
        momentumToBinario = '{0:05b}'.format(int(row[4]))
        representacionBinaria.append([capasToBinario, neuronasToBinario, epocasToBinario, learningRateToBinario, momentumToBinario])

    return representacionBinaria

def funcionCruce(padre1, padre2):
    return [ cruceOperator(padre1[0], padre2[0]), cruceOperator(padre1[1], padre2[1]),
             cruceOperator(padre1[2], padre2[2]), cruceOperator(padre1[3], padre2[3]),
             cruceOperator(padre1[4], padre2[4])]

def cruceOperator(m1, m2):
    mitad = int(len(m1)/2)
    mitadM1 = m1[:mitad]
    mitadM2 = m2[mitad:]
    hijo = "".join([ str(mitadM1) + str(mitadM2) ])
    return hijo

def mutacionOperator(poblacionConCrossOperator):
    elementoToMutar = randint(0,9)
    indiceToMutarEnNeuronas = randint(0,4)
    indiceToMutarEnEpocas = randint(0,9)
    #Aqui hacemos un aleatorio entre 1 y 2 para seleccionar el indice de neuronas o el indice de epocas
    aleatorioToSelect = randint(1,2)
    if aleatorioToSelect == 1:
        #Aqui se selecciona el indice de neuronas para mutar
        elemento = poblacionConCrossOperator[elementoToMutar]
        mutacion = elemento[1]
        valorToMutar = mutacion[indiceToMutarEnNeuronas]
        aux = list(mutacion)

        if valorToMutar == '1':
            aux[indiceToMutarEnNeuronas] = '0'
        else:
            aux[indiceToMutarEnNeuronas] = '1'

        mutacion = "".join(aux)
        elemento[1] = mutacion
        poblacionConCrossOperator[elementoToMutar] = elemento
    else:
        #Aqui se selecciona el indice de epocas para mutar
        elemento = poblacionConCrossOperator[elementoToMutar]
        mutacion = elemento[2]
        valorToMutar = mutacion[indiceToMutarEnEpocas]

        aux = list(mutacion)

        if valorToMutar == '1':
            aux[indiceToMutarEnEpocas] = '0'
        else:
            aux[indiceToMutarEnEpocas] = '1'

        mutacion = "".join(aux)
        elemento[2] = mutacion
        poblacionConCrossOperator[elementoToMutar] = elemento

    return poblacionConCrossOperator

def fitnessWeka(capas, neuronas, epocas, learRate, mom):
    learningRate = float(learRate) / 100
    momentum = float(mom) / 100

    comando = "java -cp weka.jar weka.classifiers.functions.MultilayerPerceptron -L {0} -M {1} -N {2} -V 0 -S 0 -E 20 -H {3} -t incendios.arff".format(learningRate, momentum, epocas, neuronas).split(" ")
    proceso = Popen(comando, stdout= PIPE)
    resultado = proceso.stdout.read().decode("utf-8")
    entrenamientoWeka = [ item for item in resultado.split("\n") if "Correctly Classified Instances" in item ][1].split()
    return entrenamientoWeka[-2]


def crearDescendencia(index):
    if index == 0:
        binarios = convertirABinario()
    else:
        binarios = savePoblacion

    print("Poblacion Inicial")
    print(binarios)
    #Aqui seleccionamos las parejas de padres
    padresP1P2 = [ binarios[i:i+2] for i in range(0, 10, 2) ]

    nuevosHijos1 = [ funcionCruce(row[0], row[1]) for row in padresP1P2 ]
    nuevosHijos2 = [ funcionCruce(row[1], row[0]) for row in padresP1P2 ]

    descendencia = nuevosHijos1 + nuevosHijos2
    descendenciaConMutacion = mutacionOperator(descendencia)

    print("Poblacion con cruce y muteada")
    print(descendenciaConMutacion)

    global savePoblacion
    savePoblacion = descendenciaConMutacion

    salidas = []

    for elemento in descendenciaConMutacion:
        capas = int(elemento[0], 2)
        neuronas = int(elemento[1], 2)
        epocas = int(elemento[2], 2)
        learningRate = int(elemento[3], 2)
        momentum = int(elemento[4], 2)

        if neuronas == 0:
            neuronas = 3
        if learningRate == 0:
            learningRate = 1
        if momentum == 0:
            momentum = 1

        print([capas, neuronas, epocas, learningRate, momentum])
        entrenamientoResultado = fitnessWeka(capas, neuronas, epocas, learningRate, momentum)
        salidas.append([capas, neuronas, epocas, learningRate, momentum, entrenamientoResultado])

    return salidas

if __name__ == "__main__":
    totalGeneraciones = 1
    resultadosGeneracion = []
    for i in range(0, totalGeneraciones):
        print("Generacion {0}".format(i+1))
        resultadosGeneracion.append({'resultados': crearDescendencia(i)})

    with open("salidas.csv", "a") as csvfile:
        resultado = csv.writer(csvfile, delimiter=',')
        for row in resultadosGeneracion:
            resultado.writerows(row['resultados'])

    with open('resumen.txt', 'w') as f:
        for row in resultadosGeneracion:
            f.write("%s\n" % row['resultados'])
