import csv
import json
from database import consultas
import datetime

def exportar_tabla_csv(nombre_tabla, nombre_archivo):
    func = getattr(consultas, f"obtener_{nombre_tabla}", None)
    if func is None:
        print(f"No existe función para obtener datos de {nombre_tabla}")
        return
    datos = func()
    if datos:
        with open(f"files/exp_csv/{nombre_archivo}", "w", newline='', encoding="utf-8") as f:
            escritor = csv.DictWriter(f, fieldnames=datos[0].keys())
            escritor.writeheader()
            escritor.writerows(datos)
        print(f"Exportado {nombre_tabla} a {nombre_archivo}")
    else:
        print(f"No hay datos en la tabla {nombre_tabla}")

def exportar_tabla_json(nombre_tabla, nombre_archivo):
    func = getattr(consultas, f"obtener_{nombre_tabla}", None)
    if func is None:
        print(f"No existe función para obtener datos de {nombre_tabla}")
        return
    datos = func()

    for dato in datos:
        for clave, valor in dato.items():
            if isinstance(valor, (datetime.date, datetime.datetime)):
                dato[clave] = valor.isoformat()
    if datos:
        with open(f"files/exp_json/{nombre_archivo}", "w", encoding="utf-8") as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)
        print(f"Exportado {nombre_tabla} a {nombre_archivo}")
    else:
        print(f"No hay datos en la tabla {nombre_tabla}")

def exportar_datos():
    tablas = ["alumnos", "libros", "materias", "cursos", "alumnoscrusoslibros"]
    formato = input("Elige formato de exportación (csv/json): ").lower()
    for tabla in tablas:
        archivo = f"z_{tabla}.{formato}"
        if formato == "csv":
            exportar_tabla_csv(tabla, archivo)
        elif formato == "json":
            exportar_tabla_json(tabla, archivo)
        else:
            print("Formato no soportado.")
            break