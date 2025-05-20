from files.regex import validar_dni_nie, validar_nombre
from database import consultas
from clases.enum_tramos import Tramo

def menu_alumnos():
    while True:
        print("\n--- MENÚ ALUMNOS ---")
        print("1. Ver todos los alumnos")
        print("2. Añadir alumno nuevo")
        print("3. Eliminar alumno")
        print("4. Modificar datos de un alumno")
        print("0. Volver al menú principal")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            alumnos = consultas.obtener_alumnos()
            for alumno in alumnos:
                print(f"{alumno['nie']} - {alumno['nombre']} {alumno['apellidos']} | Tramo: {alumno['tramo']} | Bilingüe: {alumno['bilingue']}")
        elif opcion == "2":
            añadir_alumno()
            print("Alumno añadido correctamente.")
        elif opcion == "3":
            nie = input("Introduce el NIE del alumno a eliminar: ").strip().upper()
            if not validar_dni_nie(nie):
                print("❌ NIE inválido.")
                continue
            consultas.eliminar_alumno(nie)
            print(f"Alumno {nie} eliminado correctamente.")
        elif opcion == "0":
            break
        else:
            print("Opción no válida.")



def añadir_alumno():
    print("\n--- Añadir Alumno ---")

    nie = input("NIE o DNI del alumno: ").strip().upper()
    if not validar_dni_nie(nie):
        print("❌ NIE o DNI inválido.")
        return

    nombre = input("Nombre: ").strip()
    if not validar_nombre(nombre):
        print("❌ Nombre inválido.")
        return

    apellidos = input("Apellidos: ").strip()
    if not validar_nombre(apellidos):
        print("❌ Apellidos inválidos.")
        return

    print("Opciones de tramo:")
    for tramo in Tramo:
        print(f"{tramo.name} ({tramo.value})")

    #Validando si tramo esta en el enum
    tramo_input = input("Introduce el valor del tramo (0/I/II): ").upper()
    tramo = Tramo(tramo_input) if tramo_input in Tramo._value2member_map_ else Tramo.NINGUNO

    bilingue_input = input("¿Es bilingüe? (S/N): ").upper()
    bilingue = 1 if bilingue_input == "s" else 0

    consultas.insertar_alumno(nie, nombre, apellidos, tramo, bilingue)


def modificar_alumno():
    print("\n--- Modificar Alumno ---")

    nie = input("Introduce el NIE del alumno que deseas modificar: ").strip()
    alumno = consultas.obtener_alumno_por_nie(nie)

    if not alumno:
        print("❌ Alumno no encontrado.")
        return

    print(f"Alumno actual: {alumno}")
    print("Deja vacío cualquier campo para no modificarlo.")

    nuevo_nombre = input(f"Nuevo nombre [{alumno['nombre']}]: ").strip() or alumno['nombre']
    nuevos_apellidos = input(f"Nuevos apellidos [{alumno['apellidos']}]: ").strip() or alumno['apellidos']

    print("Opciones de tramo: 0, I, II")
    nuevo_tramo = input(f"Nuevo tramo [{alumno['tramo']}]: ").strip().upper() or alumno['tramo']
    if nuevo_tramo not in Tramo._value2member_map_:
        print("Tramo no válido, se mantiene el anterior.")
        nuevo_tramo = alumno['tramo']

    nuevo_bilingue = input(f"Bilingüe (S/N) [{alumno['bilingue']}]: ").strip().upper()
    if nuevo_bilingue not in ("S", "N", ""):
        print("Valor no válido. Se mantiene el valor anterior.")
        nuevo_bilingue = alumno['bilingue']
    elif nuevo_bilingue == "":
        nuevo_bilingue = alumno['bilingue']

    consultas.modificar_alumno(nie, nuevo_nombre, nuevos_apellidos, nuevo_tramo, nuevo_bilingue)