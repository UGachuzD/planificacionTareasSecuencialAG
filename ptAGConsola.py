import random
import json
import warnings
import matplotlib.pyplot as plt
from tabulate import tabulate

# Variables globales para los datos
tiemposOperaciones = {
    'O1': [3.5, 6.7, 2.5, 8.2],
    'O2': [5.5, 4.2, 7.6, 9.0],
    'O3': [6.1, 7.3, 5.5, 6.7],
    'O4': [4.8, 5.3, 3.8, 4.7],
    'O5': [3.8, 3.4, 4.2, 3.6]
}

trabajos = {
    'j1': ['O2', 'O4', 'O5'],
    'j2': ['O1', 'O3', 'O5'],
    'j3': ['O1', 'O2', 'O3', 'O4', 'O5'],
    'j4': ['O4', 'O5'],
    'j5': ['O2', 'O4'],
    'j6': ['O1', 'O2', 'O4', 'O5']
}

# Parámetros del algoritmo genético
tamPoblacion = 20
generaciones = 100
tasaMutacion = 0.1
tasaCruce = 0.8

# Función para generar una planificación aleatoria
def generarPlanificacion():
    planificacion = []
    for trabajo, operaciones in trabajos.items():
        asignacionMaquinas = [random.choice(range(1, len(tiemposOperaciones[operacion]) + 1)) for operacion in operaciones]
        planificacion.append((trabajo, asignacionMaquinas))
    return planificacion

# Función para evaluar el makespan de una planificación y guardar los tiempos de inicio y fin
def evaluarPlanificacion(planificacion):
    numero_maquinas = len(next(iter(tiemposOperaciones.values())))
    tiemposMaquinas = [0] * (numero_maquinas + 1) 
    tiemposFinTrabajos = {trabajo: 0 for trabajo in trabajos.keys()} 
    tiemposTrabajos = [] 
    for trabajo, asignacionMaquinas in planificacion:
        tiempoInicioTrabajo = tiemposFinTrabajos[trabajo]
        for i, operacion in enumerate(trabajos[trabajo]):
            maquina = asignacionMaquinas[i]
            tiempoInicio = max(tiempoInicioTrabajo, tiemposMaquinas[maquina])
            tiempoFin = tiempoInicio + tiemposOperaciones[operacion][maquina-1]
            tiemposTrabajos.append((trabajo, operacion, maquina, tiempoInicio, tiempoFin))
            tiempoInicioTrabajo = tiempoFin
            tiemposMaquinas[maquina] = tiempoFin
        tiemposFinTrabajos[trabajo] = tiempoInicioTrabajo
    return max(tiemposMaquinas), tiemposTrabajos

# Función de selección por torneo
def seleccionTorneo(poblacion, puntajes, k=2):
    seleccionados = random.sample(list(zip(poblacion, puntajes)), k)
    seleccionados.sort(key=lambda x: x[1])
    return seleccionados[0][0]

# Función de cruce (Cruza de un punto)
def cruce(padre1, padre2):
    punto = random.randint(1, len(padre1)-1)
    hijo1 = padre1[:punto] + padre2[punto:]
    hijo2 = padre2[:punto] + padre1[punto:]
    return hijo1, hijo2

# Función de mutación
def mutacion(planificacion):
    trabajo, asignacionMaquinas = random.choice(planificacion)
    indice = random.randint(0, len(asignacionMaquinas)-1)
    asignacionMaquinas[indice] = random.choice(range(1, len(tiemposOperaciones[trabajos[trabajo][indice]]) + 1))

# Algoritmo genético
def algoritmoGenetico(tamPoblacion, generaciones, tasaMutacion, tasaCruce):
    poblacion = [generarPlanificacion() for _ in range(tamPoblacion)]
    
    for generacion in range(generaciones):
        puntajesYtiempos = [evaluarPlanificacion(ind) for ind in poblacion]
        puntajes = [puntaje for puntaje, _ in puntajesYtiempos]
        nuevaPoblacion = []
        for _ in range(tamPoblacion // 2):
            padre1 = seleccionTorneo(poblacion, puntajes)
            padre2 = seleccionTorneo(poblacion, puntajes)
            if random.random() < tasaCruce:
                hijo1, hijo2 = cruce(padre1, padre2)
            else:
                hijo1, hijo2 = padre1, padre2
            if random.random() < tasaMutacion:
                mutacion(hijo1)
            if random.random() < tasaMutacion:
                mutacion(hijo2)
            nuevaPoblacion.extend([hijo1, hijo2])
        poblacion = nuevaPoblacion

    mejorPlanificacion = min(poblacion, key=lambda ind: evaluarPlanificacion(ind)[0])
    mejorPuntaje, tiemposTrabajos = evaluarPlanificacion(mejorPlanificacion)
    return mejorPlanificacion, mejorPuntaje, tiemposTrabajos

# Función para graficar el cronograma de los trabajos
def graficarCronograma(tiemposTrabajos):
    # Determinar el número de máquinas en base al primer elemento de tiemposOperaciones
    numero_maquinas = len(next(iter(tiemposOperaciones.values())))
    etiquetas_maquinas = [f'M{i+1}' for i in range(numero_maquinas)]

    # Obtener una lista de colores
    colores = plt.cm.get_cmap('tab20', len(trabajos))

    fig, ax = plt.subplots(figsize=(10, 6))

    for trabajo, operacion, maquina, inicio, fin in tiemposTrabajos:
        color = colores(list(trabajos.keys()).index(trabajo))
        ax.barh(maquina-1, fin - inicio, left=inicio, color=color, edgecolor='black', label=trabajo)

    ax.set_xlabel('Tiempo')
    ax.set_ylabel('Máquina')
    ax.set_yticks(range(numero_maquinas))
    ax.set_yticklabels(etiquetas_maquinas)

    # Manejo de leyendas
    handles, labels = ax.get_legend_handles_labels()
    porEtiqueta = dict(zip(labels, handles))
    ax.legend(porEtiqueta.values(), porEtiqueta.keys())

    plt.title('Cronograma de ejecución de los trabajos')
    plt.show()

# Función para cargar datos desde un archivo JSON
def cargarDatosJSON(file_path):
    try:
        with open(file_path, 'r') as file:
            datos = json.load(file)
            tiemposOperaciones_local = datos['tiemposOperaciones']
            trabajos_local = datos['trabajos']
            print("Datos cargados desde el archivo JSON.")
            return tiemposOperaciones_local, trabajos_local
    except FileNotFoundError:
        print("Archivo no encontrado. Intente de nuevo.")
        return None, None
    except json.JSONDecodeError:
        print("Error al decodificar el archivo JSON. Asegúrese de que el archivo esté en el formato correcto.")
        return None, None

# Función del menú
def menu():
    global tiemposOperaciones, trabajos
    while True:
        print("Menú:")
        print("1. Usar datos predefinidos")
        print("2. Cargar datos desde JSON")
        print("3. Ejecutar el algoritmo genético")
        print("4. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            # Restaurar datos predefinidos
            tiemposOperaciones = {
                'O1': [3.5, 6.7, 2.5, 8.2],
                'O2': [5.5, 4.2, 7.6, 9.0],
                'O3': [6.1, 7.3, 5.5, 6.7],
                'O4': [4.8, 5.3, 3.8, 4.7],
                'O5': [3.8, 3.4, 4.2, 3.6]
            }

            trabajos = {
                'j1': ['O2', 'O4', 'O5'],
                'j2': ['O1', 'O3', 'O5'],
                'j3': ['O1', 'O2', 'O3', 'O4', 'O5'],
                'j4': ['O4', 'O5'],
                'j5': ['O2', 'O4'],
                'j6': ['O1', 'O2', 'O4', 'O5']
            }

            print("Usando datos predefinidos.")
        elif opcion == '2':
            file_path = input("Ingrese la ruta del archivo JSON: ")
            tiemposOperaciones_local, trabajos_local = cargarDatosJSON(file_path)
            if tiemposOperaciones_local and trabajos_local:
                tiemposOperaciones = tiemposOperaciones_local
                trabajos = trabajos_local
        elif opcion == '3':
            main()
        elif opcion == '4':
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

# Función principal
def main():
    random.seed(7)
    mejorPlanificacion, mejorPuntaje, tiemposTrabajos = algoritmoGenetico(tamPoblacion, generaciones, tasaMutacion, tasaCruce)

    print("Mejor planificación:", mejorPlanificacion)
    print("Makespan:", mejorPuntaje)

    # Graficar el cronograma de los trabajos
    graficarCronograma(tiemposTrabajos)

    # Crear la tabla de reporte
    tablaReporte = []
    for trabajo, operacion, maquina, inicio, fin in tiemposTrabajos:
        tiempo = fin - inicio
        tablaReporte.append([f'M{maquina}', f'{trabajo}/{operacion}', inicio, fin, tiempo])

    # Imprimir la tabla de reporte
    print(tabulate(tablaReporte, headers=['Máquina', 'Trabajos/Operaciones', 'Tiempo Inicial', 'Tiempo Final', 'Tiempo Total'], tablefmt='grid'))

# Ejecutar el menú
if __name__ == "__main__":
    menu()
