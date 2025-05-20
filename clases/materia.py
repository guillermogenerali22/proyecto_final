class Materia:
    def __init__(self, id_materia, nombre, departamento):
        self.id = id_materia
        self.nombre = nombre
        self.departamento = departamento

    def __str__(self):
        return f"{self.nombre} - Departamento: {self.departamento}"
