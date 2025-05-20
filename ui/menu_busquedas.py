from database import consultas

def menu_busquedas():
    while True:
        print("\n--- MENÚ DE BÚSQUEDAS AVANZADAS ---")
        print("1. Buscar por NIE")
        print("2. Buscar por nombre o apellidos")
        print("3. Buscar por curso")
        print("4. Buscar por ISBN")
        print("5. Buscar por estado (P/D)")
        print("0. Volver al menú principal")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            nie = input("NIE: ")
            resultados = consultas.buscar_prestamos_por_nie(nie)
        elif opcion == "2":
            nombre = input("Nombre o apellidos: ".lower().strip())
            resultados = consultas.buscar_prestamos_por_nombre(nombre)
        elif opcion == "3":
            curso = input("Curso: ".lower().strip())
            resultados = consultas.buscar_prestamos_por_curso(curso)
        elif opcion == "4":
            isbn = input("ISBN: ".lower().strip())
            resultados = consultas.buscar_prestamos_por_isbn(isbn)
        elif opcion == "5":
            estado = input("Estado (P/D): ").upper()
            resultados = consultas.buscar_prestamos_por_estado(estado)
        elif opcion == "0":
            break
        else:
            print("Opción no válida.")
            continue

        if resultados:
            for r in resultados:
                print(f"Alumno: {r['nie']} | Curso: {r['curso']} | Libro: {r['isbn']} | Estado: {r['estado']} | Fecha entrega: {r['fecha_entrega']} | Fecha devolución: {r['fecha_devolucion']}")
        else:
            print("No se encontraron resultados.")