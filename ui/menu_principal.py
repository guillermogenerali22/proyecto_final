import config
from database import consultas
from ui import menu_general, menu_alumnos, menu_cursos_materias, menu_libros, menu_prestamos, menu_busquedas, menu_BBDD



def login():
    print("=== INICIO DE SESIÓN ===")
    usuario = input("Usuario: ")
    contrasena = input("Contraseña: ")

    if usuario == config.APP_ADMIN_USER and contrasena == config.APP_ADMIN_PASS:
        print("Login correcto.\n")
        return True
    else:
        print("Credenciales incorrectas.\n")
        return False


def mostrar_menu_principal():

    nombre_BBDD = input("¿Cual es el nombre de la BBDD?: ")

    while True:
        print("\n===== MENÚ PRINCIPAL =====")
        print("1. Gestión General")
        print("2. Alumnos")
        print("3. Cursos y Materias")
        print("4. Libros")
        print("5. Préstamos")
        print("6. Buscar préstamos por filtro")
        print("7. Base de Datos")
        print("0. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            menu_general.menu_general()
        elif opcion == "2":
            menu_alumnos.menu_alumnos()
        elif opcion == "3":
            menu_cursos_materias.menu_cursos_materias()
        elif opcion == "4":
            menu_libros.menu_libros()
        elif opcion == "5":
            menu_prestamos.menu_prestamos()
        elif opcion == "6":
            menu_busquedas.menu_busquedas()
        elif opcion == "7":
            menu_BBDD.menu_BBDD()
        elif opcion == "0":
            print("Saliendo del programa...")
            break
        elif opcion == "9":
            consultas.ver_todos_los_datos()
        else:
            print("Opción no válida. Intenta de nuevo.")
