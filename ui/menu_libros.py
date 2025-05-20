from database import consultas
from files.regex import validar_isbn, validar_nombre

def menu_libros():
    while True:
        print("\n--- MENÚ LIBROS ---")
        print("1. Ver libros")
        print("2. Añadir libro")
        print("0. Volver al menú principal")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            libros = consultas.obtener_libros()
            for libro in libros:
                print(f"{libro['isbn']} - {libro['titulo']} | Autor: {libro['autor']} | Ejemplares: {libro['numero_ejemplares']}")
        elif opcion == "2":
            añadir_libro()
        elif opcion == "0":
            break
        else:
            print("Opción no válida.")


def añadir_libro():
    print("\n--- Añadir Libro ---")

    isbn = input("ISBN del libro: ").strip()
    if not validar_isbn(isbn):
        print("❌ ISBN inválido.")
        return

    titulo = input("Título: ").strip()
    if not validar_nombre(titulo):
        print("❌ Título inválido.")
        return

    autor = input("Autor: ").strip()
    if not validar_nombre(autor):
        print("❌ Autor inválido.")
        return

    try:
        ejemplares = int(input("Número de ejemplares: "))
    except ValueError:
        print("❌ Número de ejemplares inválido.")
        return

    try:
        id_materia = int(input("ID de materia: "))
        id_curso = int(input("ID de curso: "))
    except ValueError:
        print("❌ ID de materia o curso inválido.")
        return

    consultas.insertar_libro(isbn, titulo, autor, ejemplares, id_materia, id_curso)