import csv
from database import consultas

def exportar_tabla_csv(nombre_tabla, nombre_archivo):
    # llamando a funciones de obtener en consultas.py
    func = getattr(consultas, f"obtener_{nombre_tabla}", None)
    if func is None:
        print(f"No existe función para obtener datos de {nombre_tabla}")
        return
    datos = func()
    if datos:
        with open(nombre_archivo, "w", newline='', encoding="utf-8") as f:
            escritor = csv.DictWriter(f, fieldnames=datos[0].keys())
            escritor.writeheader()
            escritor.writerows(datos)
        print(f"Exportado {nombre_tabla} a {nombre_archivo}")
    else:
        print(f"No hay datos en la tabla {nombre_tabla}")

def hacer_backup_csv():
    tablas = ["alumnos", "libros", "materias", "cursos", "alumnoscrusoslibros"]
    for tabla in tablas:
        archivo = f"files/csv/backup_{tabla}.csv"
        exportar_tabla_csv(tabla, archivo)