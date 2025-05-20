class Libro:
    def __init__(self, isbn, titulo, autor, numero_ejemplares, id_materia, id_curso):
        self.isbn = isbn
        self.titulo = titulo
        self.autor = autor
        self.numero_ejemplares = numero_ejemplares
        self.id_materia = id_materia
        self.id_curso = id_curso

    def __str__(self):
        return f"{self.titulo} - {self.autor} (ISBN: {self.isbn})"
