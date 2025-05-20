from database import consultas
from files import backup

def menu_BBDD():
    while True:
        print("\n--- MENÚ BBDD ---")
        print("1. Hacer backup de la base de datos")
        print("2. Vaciar BBDD")
        print("0. Volver al menú principal")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            backup.hacer_backup_csv()
            print("Backup realizado con éxito.")
        elif opcion == "2":
            consultas.vaciar_base_de_datos()
            print("Base de datos vaciada con éxito.")
        elif opcion == "0":
            break
        else:
            print("Opción no válida.")