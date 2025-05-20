import re

regex_nombre = re.compile(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ\s\-']+$")
regex_isbn = re.compile(r"^(?:\d{9}[\dXx]|\d{13})$")
regex_dni_nie = re.compile(r"^(?:\d{8}[A-Z]|[XYZ]\d{7}[A-Z])$")

def validar_nombre(nombre):
    return bool(regex_nombre.match(nombre.strip()))

def validar_isbn(isbn):
    isbn_limpio = isbn.replace("-", "").replace(" ", "")
    return bool(regex_isbn.match(isbn_limpio))

def validar_dni_nie(valor):
    valor = valor.strip().upper()
    return bool(regex_dni_nie.match(valor))