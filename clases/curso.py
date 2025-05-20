class Curso:
    def __init__(self, curso, nivel):
        self.curso = curso
        self.nivel = nivel

    def __str__(self):
        return f"{self.nivel} ({self.curso})"
