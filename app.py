from ui.menu_principal import mostrar_menu_principal, login

def main():
    if login():
        mostrar_menu_principal()
    else:
        print("No se pudo acceder al sistema.")

if __name__ == "__main__":
    main()