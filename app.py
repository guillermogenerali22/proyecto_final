from ui.menu_principal import mostrar_menu_principal, login

def main():
    if login():
        mostrar_menu_principal()
    else:
        print("No se pudo acceder al sistema.")

if __name__ == "__main__":
    main()

#TODO MIRAR DIAGRAMA DE ACTIVIDADES. (VACIARBBD, GESTION LISTADOS, GESTION ERRORES, SUBCASO.)

#todo diagrama de clases pasar a diagram.io
#todo falta hacer funcional la validacion de fechas (que no pueda haber una devolucion de \n
# prestamo de una fecha anterior a la fecha de entrega.