from database import consultas

def menu_cursos_materias():
    while True:
        print("\n--- MENÚ CURSOS Y MATERIAS ---")
        print("1. Ver cursos")
        print("2. Ver materias")
        print("0. Volver al menú principal")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            cursos = consultas.obtener_cursos()
            for curso in cursos:
                print(f"{curso['curso']} - Nivel: {curso['nivel']}")
        elif opcion == "2":
            materias = consultas.obtener_materias()
            for materia in materias:
                print(f"{materia['id']} - {materia['nombre']} | Departamento: {materia['departamento']}")
        elif opcion == "0":
            break
        else:
            print("Opción no válida.")
