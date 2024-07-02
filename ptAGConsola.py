import random
import json
import warnings
import matplotlib.pyplot as plt
from tabulate import tabulate
warnings.filterwarnings("ignore")

"""
    Datos por defecto que pueden llenarse a mano:
"""
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

""" 
    Parametros del algoritmo genético:
"""
tamPoblacion = 20
generaciones = 100
tasaMutacion = 0.1
tasaCruce = 0.8

def generarPlanificacion():
    """
    Genera una planificación de trabajos asignando aleatoriamente las operaciones a las máquinas disponibles.

    Returns:
        list: Una lista de tuplas que representa la planificación generada. Cada tupla contiene el nombre del trabajo y una lista de asignaciones 
        de máquinas para cada operación del trabajo.
    """
    planificacion = []
    for trabajo, operaciones in trabajos.items():
        asignacionMaquinas = [random.choice(range(1, len(tiemposOperaciones[operacion]) + 1)) for operacion in operaciones]
        planificacion.append((trabajo, asignacionMaquinas))
    return planificacion


def evaluarPlanificacion(planificacion):
    """
    Evalúa una planificación dada y devuelve el tiempo máximo de finalización de las máquinas y los tiempos de inicio y finalización de cada trabajo.

    Args:
        planificacion (list): Una lista de tuplas que representan la asignación de máquinas a cada trabajo. Cada tupla contiene el nombre del trabajo 
        y una lista de asignaciones de máquinas para cada operación del trabajo.

    Returns:
        tuple: Una tupla que contiene el tiempo máximo de finalización de las máquinas y una lista de tuplas que representan los tiempos de inicio y 
        finalización de cada trabajo. Cada tupla contiene el nombre del trabajo, el nombre de la operación, el número de la máquina, el tiempo de inicio 
        y el tiempo de finalización.
    """
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


def seleccionTorneo(poblacion, puntajes, k=2):
    """
    Selecciona individuos de la población mediante el método del torneo.

    Args:
        poblacion (list): Una lista de individuos de la población.
        puntajes (list): Una lista de puntajes correspondientes a los individuos de la población.
        k (int): El número de individuos a seleccionar en cada torneo. Por defecto es 2.

    Returns:
        object: El individuo seleccionado con el puntaje más bajo.

    """
    seleccionados = random.sample(list(zip(poblacion, puntajes)), k)
    seleccionados.sort(key=lambda x: x[1])
    return seleccionados[0][0]


def cruce(padre1, padre2):
    """
    Realiza el cruce de dos padres para generar dos hijos.

    Args:
        padre1 (list): Lista que representa el primer padre.
        padre2 (list): Lista que representa el segundo padre.

    Returns:
        tuple: Una tupla que contiene los dos hijos generados.
    """
    punto = random.randint(1, len(padre1)-1)
    hijo1 = padre1[:punto] + padre2[punto:]
    hijo2 = padre2[:punto] + padre1[punto:]
    return hijo1, hijo2


def mutacion(planificacion):
    """
    Realiza una mutación en la planificación dada.

    Args:
        planificacion (list): Una lista que representa la planificación actual.

    Returns:
        None

    """
    trabajo, asignacionMaquinas = random.choice(planificacion)
    indice = random.randint(0, len(asignacionMaquinas)-1)
    asignacionMaquinas[indice] = random.choice(range(1, len(tiemposOperaciones[trabajos[trabajo][indice]]) + 1))


def algoritmoGenetico(tamPoblacion, generaciones, tasaMutacion, tasaCruce):
    """
    Implementa el algoritmo genético para la planificación de tareas secuencial.
    
    Args:
        tamPoblacion (int): El tamaño de la población de individuos.
        generaciones (int): El número de generaciones a evolucionar.
        tasaMutacion (float): La probabilidad de mutación de un individuo.
        tasaCruce (float): La probabilidad de cruce entre dos individuos.
    
    Returns:
        tuple: Una tupla que contiene la mejor planificación encontrada, el puntaje de la mejor planificación y los tiempos de los trabajos.
    """
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


def graficarCronograma(tiemposTrabajos):
    """
    Genera un gráfico de barras horizontal que muestra el cronograma de ejecución de los trabajos en diferentes máquinas.

    Args:
        tiemposTrabajos (list): Una lista de tuplas que contienen información sobre cada trabajo, operación, máquina, inicio y fin.

    Returns:
        None
    """
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


def cargarDatosJSON(file_path):
    """
    Carga los datos desde un archivo JSON.

    Args:
        file_path (str): La ruta del archivo JSON.

    Returns:
        tuple: Una tupla que contiene los tiempos de operaciones y los trabajos cargados desde el archivo JSON.
           Si el archivo no se encuentra o no se puede decodificar, se devuelve (None, None).
    """
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


def menu():
    """
        Muestra un menú de opciones y permite al usuario seleccionar una opción.
        Las opciones incluyen usar datos predefinidos, cargar datos desde un archivo JSON,
        ejecutar el algoritmo genético y salir del programa.
    """
    global tiemposOperaciones, trabajos
    while True:
        print("Menú:")
        print("1. Usar datos predefinidos")
        print("2. Cargar datos desde JSON")
        print("3. Ejecutar el algoritmo genético")
        print("4. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            # Restaurar datos predefinidos porque sino se queda con los ultimos datos cargados
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


def main():
    """
    Función principal del programa que ejecuta el algoritmo genético para encontrar la mejor planificación de tareas.

    Parameters:
        None

    Returns:
        None
    """
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

"""
    Ejecutar el programa
"""
if __name__ == "__main__":
    menu()
