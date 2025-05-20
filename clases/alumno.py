from clases.enum_tramos import Tramo

class Alumno:
    def __init__(self, nie, nombre, apellidos, tramo: Tramo, bilingue: bool):
        self.nie = nie
        self.nombre = nombre
        self.apellidos = apellidos
        self.tramo = tramo if tramo in tramo else Tramo.NINGUNO
        self.bilingue = bilingue

    def __str__(self):
        return f"{self.nombre} {self.apellidos} ({self.nie}) - Tramo: {self.tramo.value} - Bilingüe: {self.bilingue}"
