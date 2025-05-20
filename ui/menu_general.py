def menu_general():
    while True:
        print("\n--- MENÚ GENERAL ---")
        print("1. Cargar datos desde CSV")
        print("2. Hacer copia de seguridad CSV")
        print("3. Exportar datos CSV/JSON")
        print("0. Volver al menú principal")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            from files import cargainicial
            cargainicial.cargar_todo()
        elif opcion == "2":
            from files import backup
            backup.hacer_backup_csv()
        elif opcion == "3":
            from files import exportacion
            exportacion.exportar_datos()
        elif opcion == "0":
            break
        else:
            print("Opción no válida.")