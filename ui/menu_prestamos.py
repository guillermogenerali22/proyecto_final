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

    prestamos_cerrados = consultas.obtener_prestamos_cerrados()

    if not prestamos_cerrados:
        print("❌ No hay préstamos cerrados disponibles.")
        return

    print("\n--- Préstamos Cerrados Disponibles ---")
    for i, p in enumerate(prestamos_cerrados, 1):
        print(f"{i}. NIE: {p['nie']} | Curso: {p['curso']} | ISBN: {p['isbn']} | Entregado: {p['fecha_entrega']} | Devuelto: {p['fecha_devolucion']}")

    try:
        seleccion = int(input("Selecciona un préstamo para generar el contrato (número): "))
        if not (1 <= seleccion <= len(prestamos_cerrados)):
            print("❌ Selección inválida.")
            return
        prestamo = prestamos_cerrados[seleccion - 1]
    except ValueError:
        print("❌ Entrada no válida.")
        return

    # Aquí va tu lógica de generación de contrato
    print(f"\n📝 Generando contrato para:")
    print(f"NIE: {prestamo['nie']}, ISBN: {prestamo['isbn']}, Curso: {prestamo['curso']}")
