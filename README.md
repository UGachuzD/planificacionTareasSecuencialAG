# planificacionTareasSecuencialAG
Proyecto final | Algoritmos bioinspirados | Planificación de tareas secuencial | Python

# Proyecto de Algoritmo Genético para la Planificación de Tareas

## Descripción
Este proyecto implementa un algoritmo genético para la planificación de tareas. Utiliza diferentes máquinas para ejecutar las operaciones de varios trabajos y busca minimizar el tiempo total de ejecución (makespan).

## Requisitos
Antes de ejecutar el script, asegúrate de tener instaladas las siguientes dependencias:

- Python 3.x
- Matplotlib
- Tabulate

Puedes instalar estas dependencias usando pip:

```bash
pip install matplotlib tabulate
```
## Archivos

-   `main.py`: Contiene el código principal del algoritmo genético y las funciones auxiliares.
-   `data.json` (opcional): Archivo JSON que contiene los datos de `tiemposOperaciones` y `trabajos`. Si no se proporciona, se utilizarán los datos predefinidos en el script.

## Ejecución

Para ejecutar el script, sigue los siguientes pasos:

1.  Guarda el código proporcionado en un archivo llamado `main.py`.
    
2.  Ejecuta el archivo `main.py` desde la línea de comandos:
    


```bash
python main.py 
```
3.  El menú principal te proporcionará las siguientes opciones:
    1.  Usar datos predefinidos.
    2.  Cargar datos desde un archivo JSON.
    3.  Ejecutar el algoritmo genético.
    4.  Salir.

### Opción 1: Usar datos predefinidos

Selecciona esta opción para utilizar los datos predefinidos en el script.

### Opción 2: Cargar datos desde un archivo JSON

Selecciona esta opción para cargar datos desde un archivo JSON. Se te pedirá que ingreses la ruta del archivo JSON (En caso de que este en la raiz unicamente escribir el nombre del archivo con la extension json. Ej: datos.json y dar enter). Asegúrate de que el archivo JSON tenga el siguiente formato:

```json
{
"tiemposOperaciones": {
"O1": [3.5, 6.7, 2.5, 8.2],
"O2": [5.5, 4.2, 7.6, 9.0],
"O3": [6.1, 7.3, 5.5, 6.7],
"O4": [4.8, 5.3, 3.8, 4.7],
"O5": [3.8, 3.4, 4.2, 3.6]
},
"trabajos": {
"j1": ["O2", "O4", "O5"],
"j2": ["O1", "O3", "O5"],
"j3": ["O1", "O2", "O3", "O4", "O5"],
"j4": ["O4", "O5"],
"j5": ["O2", "O4"],
"j6": ["O1", "O2", "O4", "O5"]
}
}
```

### Opción 3: Ejecutar el algoritmo genético

Selecciona esta opción para ejecutar el algoritmo genético con los datos actuales (Ya sea que antes se selecciono usar los datos del programa o los del JSON). El programa mostrará la mejor planificación encontrada y el makespan correspondiente. Además, se generará un cronograma gráfico de la ejecución de los trabajos.

### Opción 4: Salir

Selecciona esta opción para salir del programa.

## Contacto

Para cualquier consulta o sugerencia, por favor contacta a ulisesgachuz07@gmail.com.
