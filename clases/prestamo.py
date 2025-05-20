from datetime import date
from clases.enum_estados import EstadoPrestamo

class Prestamo:
    def __init__(self, nie_alumno, curso, isbn, fecha_entrega: date, fecha_devolucion: date, estado: EstadoPrestamo):
        self.nie_alumno = nie_alumno
        self.curso = curso
        self.isbn = isbn
        self.fecha_entrega = fecha_entrega
        self.fecha_devolucion = fecha_devolucion
        self.estado = estado if estado in EstadoPrestamo else EstadoPrestamo.PRESTADO

    def __str__(self):
        return f"Préstamo de {self.isbn} a {self.nie_alumno} - Estado: {self.estado.value}"
