import csv
from database import consultas
from clases.enum_tramos import Tramo

def cargar_materias_csv(path):
    with open(path, encoding='utf-8') as file:
        lector = csv.DictReader(file)
        for fila in lector:
            consultas.insertar_materia(int(fila["id"]), fila["nombre"], fila["departamento"])

def cargar_cursos_csv(path):
    with open(path, encoding='utf-8') as file:
        lector = csv.DictReader(file)
        for fila in lector:
            consultas.insertar_curso(fila["curso"], fila["nivel"])

def cargar_libros_csv(path):
    with open(path, encoding='utf-8') as file:
        lector = csv.DictReader(file)
        for fila in lector:
            consultas.insertar_libro(
                fila["isbn"],
                fila["titulo"],
                fila["autor"],
                int(fila["numero_ejemplares"]),
                int(fila["id_materia"]),
                fila["id_curso"]
            )

def cargar_alumnos_csv(path):
    with open(path, encoding='utf-8') as file:
        lector = csv.DictReader(file)
        for fila in lector:
            tramo_enum = Tramo(fila["tramo"]) if fila["tramo"] in Tramo._value2member_map_ else Tramo.NINGUNO
            bilingue_bool = fila["bilingue"].strip().upper() in ["1", "TRUE", "S", "SI"]
            consultas.insertar_alumno(
                fila["nie"],
                fila["nombre"],
                fila["apellidos"],
                tramo_enum,
                bilingue_bool
            )
def cargar_alumnoscrusoslibros_csv(path):
    with open(path, encoding='utf-8') as file:
        lector = csv.DictReader(file)
        for fila in lector:
            consultas.insertar_alumnoscrusoslibros(
                fila["nie"],
                fila["curso"],
                fila["isbn"],
                fila["fecha_entrega"],
                fila["fecha_devolucion"],
                fila["estado"]
            )

def cargar_todo():
    print("Vaciando base de datos antes de cargar los datos iniciales...")
    consultas.vaciar_base_de_datos()

    cargar_materias_csv("files/up_csv/up_materias.csv")
    cargar_cursos_csv("files/up_csv/up_cursos.csv")
    cargar_alumnos_csv("files/up_csv/up_alumnos.csv")
    cargar_libros_csv("files/up_csv/up_libros.csv")
    cargar_alumnoscrusoslibros_csv("files/up_csv/up_alumnoscrusoslibros.csv")

    print("✅ Datos cargados correctamente.")

if __name__ == "__main__":
    cargar_todo()
    print("Carga de datos completada con éxito.")
