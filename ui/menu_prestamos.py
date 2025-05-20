from database import consultas
from clases.enum_estados import EstadoPrestamo
from datetime import datetime

def menu_prestamos():
    while True:
        print("\n--- MENÚ PRÉSTAMOS ---")
        print("1. Ver todos los préstamos")
        print("2. Registrar nuevo préstamo")
        print("3. Generar contrato de préstamo")
        print("4. Cerrar préstamo")
        print("0. Volver al menú principal")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            prestamos = consultas.obtener_prestamos()
            for p in prestamos:
                print(f"Alumno: {p['nie']} | Curso: {p['curso']} | Libro: {p['isbn']} | Entrega: {p['fecha_entrega']} | Devolución: {p['fecha_devolucion']} | Estado: {p['estado']}")
        elif opcion == "2":
            # Mostrar datos necesarios para registrar el préstamo
            print("\nLista de Alumnos:")
            alumnos = consultas.obtener_alumnos()
            for alumno in alumnos:
                print(f"NIE: {alumno['nie']} - {alumno['nombre']} {alumno['apellidos']}")

            print("\nLista de Cursos:")
            cursos = consultas.obtener_cursos()
            for curso in cursos:
                print(f"Curso: {curso['curso']} - Nivel: {curso['nivel']}")

            print("\nLista de Libros:")
            libros = consultas.obtener_libros()
            for libro in libros:
                print(f"ISBN: {libro['isbn']} - Título: {libro['titulo']} - Ejemplares: {libro['numero_ejemplares']}")

            # Ahora pedir datos para registrar
            nie = input("\n Introduce el NIE del alumno: ".lower().strip())
            curso = input("Introduce el curso: ".lower().strip())
            isbn = input("Introduce el ISBN del libro: ".lower().strip())
            fecha_entrega = input("Fecha de entrega (YYYY-MM-DD): ")
            fecha_devolucion = input("Fecha de devolución (YYYY-MM-DD): ")
            estado = "Prestado " # Por defecto, se considera prestado
            estado_enum = EstadoPrestamo(estado) if estado in EstadoPrestamo._value2member_map_ else EstadoPrestamo.PRESTADO

            if consultas.registrar_prestamo(nie, curso, isbn, fecha_entrega, fecha_devolucion, estado_enum):
                print("Préstamo registrado correctamente.")
            pass
        elif opcion == "3":
            generar_contrato()
            print("Contrato generado.")
        elif opcion == "4":
            nie = input("NIE del alumno: ")
            curso = input("Curso: ")
            consultas.cerrar_prestamo(nie, curso)
            print("Préstamos cerrados para el alumno en el curso indicado.")
        elif opcion == "0":
            break
        else:
            print("Opción no válida.")
def generar_contrato():
    nie = input("NIE del alumno: ".lower().strip())
    prestamos = consultas.obtener_prestamos_por_nie(nie)

    if not prestamos:
        print("No se encontraron préstamos para ese alumno.")
        return

    alumno = consultas.obtener_alumno_por_nie(nie)
    fecha = datetime.now().strftime("%Y-%m-%d")
    nombre_archivo = f"files/contrato/contrato_{nie}_{fecha}.txt"

    with open(nombre_archivo, "w", encoding="utf-8") as f:
        f.write(f"CONTRATO DE PRÉSTAMO DE LIBROS\n\n")
        f.write(f"Fecha: {fecha}\n")
        f.write(f"Alumno: {alumno['nombre']} {alumno['apellidos']} (NIE: {nie})\n")
        f.write(f"Tramo: {alumno['tramo']} | Bilingüe: {alumno['bilingue']}\n\n")
        f.write(f"Libros asignados:\n")
        for p in prestamos:
            f.write(f" - {p['isbn']} (Curso: {p['curso']}) - Estado: {p['estado']}\n")

        f.write("\nFirma del alumno: __________________________\n")
        f.write("Firma del centro: __________________________\n")

    print(f"Contrato generado: {nombre_archivo}")