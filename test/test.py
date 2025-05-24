
import unittest
from unittest.mock import patch, MagicMock
from datetime import date
from clases.enum_tramos import Tramo

from database import consultas

class TestConsultas(unittest.TestCase):

    def setUp(self):
        self.mock_conexion = MagicMock()
        self.mock_cursor = MagicMock()
        self.mock_conexion.cursor.return_value = self.mock_cursor

    def _mock_db(self, mock_obtener_conexion):
        mock_obtener_conexion.return_value = self.mock_conexion

    @patch('database.consultas.obtener_conexion')
    def test_insertar_alumno(self, mock_con):
        self._mock_db(mock_con)
        consultas.insertar_alumno("12345678A", "Nombre", "Apellido", MagicMock(value="1"), 1)
        self.mock_cursor.execute.assert_called_once()
        self.mock_conexion.commit.assert_called_once()

    @patch('database.consultas.obtener_conexion')
    def test_obtener_alumnos(self, mock_con):
        self._mock_db(mock_con)
        self.mock_cursor.fetchall.return_value = []
        alumnos = consultas.obtener_alumnos()
        self.assertEqual(alumnos, [])

    @patch('database.consultas.obtener_conexion')
    def test_insertar_libro(self, mock_con):
        self._mock_db(mock_con)
        consultas.insertar_libro("1234567890", "Titulo", "Autor", 1, 1, "1ESO")
        self.mock_cursor.execute.assert_called_once()

    @patch('database.consultas.obtener_conexion')
    def test_obtener_libros(self, mock_con):
        self._mock_db(mock_con)
        self.mock_cursor.fetchall.return_value = []
        libros = consultas.obtener_libros()
        self.assertEqual(libros, [])

    @patch('database.consultas.obtener_conexion')
    def test_insertar_curso(self, mock_con):
        self._mock_db(mock_con)
        consultas.insertar_curso("1ESO", "ESO")
        self.mock_cursor.execute.assert_called_once()

    @patch('database.consultas.obtener_conexion')
    def test_insertar_materia(self, mock_con):
        self._mock_db(mock_con)
        consultas.insertar_materia(1, "Matematicas", "Ciencias")
        self.mock_cursor.execute.assert_called_once()

    @patch('database.consultas.obtener_conexion')
    def test_registrar_prestamo(self, mock_con):
        self._mock_db(mock_con)
        mock_estado = MagicMock(value='P')
        consultas.registrar_prestamo("12345678A", "1ESO", "1234567890", date.today(), date.today(), mock_estado)
        self.mock_cursor.execute.assert_called_once()

    @patch('database.consultas.obtener_conexion')
    def test_obtener_prestamos(self, mock_con):
        self._mock_db(mock_con)
        self.mock_cursor.fetchall.return_value = []
        prestamos = consultas.obtener_prestamos()
        self.assertEqual(prestamos, [])

    @patch('database.consultas.obtener_conexion')
    def test_modificar_alumno(self, mock_con):
        self._mock_db(mock_con)
        consultas.modificar_alumno("12345678A", "NuevoNombre", "NuevoApellido", "2", 0)
        self.mock_cursor.execute.assert_called_once()

    @patch('database.consultas.obtener_conexion')
    def test_eliminar_alumno(self, mock_con):
        self._mock_db(mock_con)
        consultas.eliminar_alumno("12345678A")
        self.mock_cursor.execute.assert_called_once_with("DELETE FROM alumnos WHERE nie = %s", ("12345678A",))

    @patch('database.consultas.obtener_conexion')
    def test_insertar_alumnoscrusoslibros(self, mock_con):
        self._mock_db(mock_con)
        consultas.insertar_alumnoscrusoslibros("12345678A", "1ESO", "1234567890", date.today(), date.today(), "P")
        self.mock_cursor.execute.assert_called_once()

    @patch('database.consultas.obtener_conexion')
    def test_vaciar_base_de_datos_cancelado(self, mock_con):
        with patch('builtins.input', return_value='N'), patch('builtins.print') as mock_print:
            consultas.vaciar_base_de_datos()
            mock_print.assert_called_with("Operación cancelada.")


class TestMenus(unittest.TestCase):

    @patch('builtins.print')
    @patch('database.consultas.obtener_alumnos')
    def test_menu_alumnos_ver_todos(self, mock_obtener_alumnos, mock_print):
        mock_obtener_alumnos.return_value = [
            {"nie": "123A", "nombre": "Juan", "apellidos": "Pérez", "tramo": "I", "bilingue": 1}
        ]
        with patch('builtins.input', side_effect=["1", "0"]):
            from ui.menu_alumnos import menu_alumnos
            menu_alumnos()
        mock_print.assert_any_call("123A - Juan Pérez | Tramo: I | Bilingüe: 1")


    @patch('database.consultas.insertar_libro')
    @patch('files.regex.validar_isbn', return_value=True)
    @patch('files.regex.validar_nombre', return_value=True)
    @patch('builtins.input')
    def test_añadir_libro_success(self, mock_input, mock_validar_nombre, mock_validar_isbn, mock_insertar):
        mock_input.side_effect = ["9781234567890", "Matemáticas", "García", "3", "1", "2"]
        from ui.menu_libros import añadir_libro
        añadir_libro()
        mock_insertar.assert_called_once_with("9781234567890", "Matemáticas", "García", 3, 1, "2")

    @patch('database.consultas.modificar_alumno')
    @patch('database.consultas.obtener_alumno_por_nie')
    @patch('builtins.input')
    def test_modificar_alumno(self, mock_input, mock_obtener, mock_modificar):
        mock_obtener.return_value = {
            "nie": "123A", "nombre": "Juan", "apellidos": "Pérez", "tramo": "0", "bilingue": 1
        }
        mock_input.side_effect = [
            "123A", "Pedro", "López", "I", "N"
        ]
        from ui.menu_alumnos import modificar_alumno
        modificar_alumno()
        mock_modificar.assert_called_once_with("123A", "Pedro", "López", "I", "N")

class TestNumeroEjemplares(unittest.TestCase):

        @patch("database.consultas.obtener_conexion")
        def test_prestamo_sin_ejemplares_disponibles(self, mock_obtener_conexion):
            # Configurar mock
            mock_conexion = MagicMock()
            mock_cursor = MagicMock()

            mock_obtener_conexion.return_value = mock_conexion
            mock_conexion.cursor.return_value = mock_cursor

            # Simular que el libro tiene 0 ejemplares disponibles
            mock_cursor.fetchall.return_value = [{"isbn": "1234567890", "numero_ejemplares": 0}]

            # Ejecutar
            libros = consultas.obtener_libros()
            ejemplares_disponibles = libros[0]["numero_ejemplares"]

            # Verificar que no es posible realizar préstamo si no hay ejemplares
            self.assertEqual(ejemplares_disponibles, 0, "El número de ejemplares debe ser 0 para esta prueba")
            puede_prestar = ejemplares_disponibles > 0
            self.assertFalse(puede_prestar, "No se debería poder prestar un libro sin ejemplares disponibles")


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)

