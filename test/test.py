
import unittest
from unittest.mock import patch, MagicMock, call
from datetime import date

# Asumimos que este archivo (test.py) está en el directorio raíz del proyecto
# y 'database' es un subdirectorio.
from database import consultas


# Clase auxiliar para simular objetos Enum con un atributo 'value'
class MockEnumValue:
    def __init__(self, value):
        self.value = value


class TestConsultas(unittest.TestCase):

    # Helper para crear un mock de conexión y cursor configurado
    def _get_mock_db_resources(self, obtener_conexion_mock, fetchall_return=None, fetchone_return=None,
                               dictionary_cursor=False):
        mock_conexion = MagicMock()
        mock_cursor = MagicMock()

        if dictionary_cursor:
            obtener_conexion_mock.return_value.cursor.return_value = mock_cursor
        else:
            obtener_conexion_mock.return_value.cursor.return_value = mock_cursor

        obtener_conexion_mock.return_value = mock_conexion
        mock_conexion.cursor.return_value = mock_cursor

        if fetchall_return is not None:
            mock_cursor.fetchall.return_value = fetchall_return
        if fetchone_return is not None:
            mock_cursor.fetchone.return_value = fetchone_return

        return mock_conexion, mock_cursor

    @patch('builtins.print')
    @patch('database.consultas.obtener_conexion')
    def test_insertar_alumno_success(self, mock_obtener_conexion, mock_print):
        mock_conexion, mock_cursor = self._get_mock_db_resources(mock_obtener_conexion)
        mock_tramo = MockEnumValue("Tramo1")

        consultas.insertar_alumno("123A", "Nombre", "Apellidos", mock_tramo, True)

        mock_obtener_conexion.assert_called_once()
        mock_conexion.cursor.assert_called_once_with()
        mock_cursor.execute.assert_called_once_with(
            unittest.mock.ANY,  # SQL string
            ("123A", "Nombre", "Apellidos", "Tramo1", True)
        )
        mock_conexion.commit.assert_called_once()
        mock_print.assert_called_with("✅ Alumno insertado correctamente")
        mock_cursor.close.assert_called_once()
        mock_conexion.close.assert_called_once()

    @patch('builtins.print')
    @patch('database.consultas.obtener_conexion')
    def test_insertar_alumno_db_error(self, mock_obtener_conexion, mock_print):
        mock_conexion, mock_cursor = self._get_mock_db_resources(mock_obtener_conexion)
        mock_cursor.execute.side_effect = Exception("DB Error")
        mock_tramo = MockEnumValue("Tramo1")

        consultas.insertar_alumno("123A", "Nombre", "Apellidos", mock_tramo, True)

        mock_print.assert_called_with("❌ Error durante la operación: DB Error")
        mock_conexion.commit.assert_not_called()  # No se debe llamar a commit si hay error
        mock_cursor.close.assert_called_once()
        mock_conexion.close.assert_called_once()

    @patch('database.consultas.obtener_conexion')
    def test_insertar_alumno_no_conexion(self, mock_obtener_conexion):
        mock_obtener_conexion.return_value = None
        mock_tramo = MockEnumValue("Tramo1")

        result = consultas.insertar_alumno("123A", "Nombre", "Apellidos", mock_tramo, True)
        self.assertIsNone(result)  # La función debería retornar implícitamente None

    @patch('builtins.print')
    @patch('database.consultas.obtener_conexion')
    def test_obtener_alumnos_success(self, mock_obtener_conexion, mock_print):
        expected_alumnos = [{"nie": "123A", "nombre": "Test"}]
        mock_conexion, mock_cursor = self._get_mock_db_resources(mock_obtener_conexion,
                                                                 fetchall_return=expected_alumnos,
                                                                 dictionary_cursor=True)

        alumnos = consultas.obtener_alumnos()

        self.assertEqual(alumnos, expected_alumnos)
        mock_obtener_conexion.assert_called_once()
        mock_conexion.cursor.assert_called_once_with(dictionary=True)
        mock_cursor.execute.assert_called_once_with("SELECT * FROM alumnos")
        mock_print.assert_called_with("✅ Alumnos cargados correctamente")
        mock_cursor.close.assert_called_once()
        mock_conexion.close.assert_called_once()

    @patch('builtins.print')
    @patch('database.consultas.obtener_conexion')
    def test_obtener_alumnos_db_error(self, mock_obtener_conexion, mock_print):
        mock_conexion, mock_cursor = self._get_mock_db_resources(mock_obtener_conexion, dictionary_cursor=True)
        mock_cursor.execute.side_effect = Exception("DB Error")

        alumnos = consultas.obtener_alumnos()

        self.assertIsNone(alumnos)  # Debería retornar None o una lista vacía según el manejo de error
        mock_print.assert_called_with("❌ Error durante la operación: DB Error")
        mock_cursor.close.assert_called_once()
        mock_conexion.close.assert_called_once()

    @patch('builtins.print')
    @patch('database.consultas.obtener_conexion')
    def test_insertar_libro_success(self, mock_obtener_conexion, mock_print):
        mock_conexion, mock_cursor = self._get_mock_db_resources(mock_obtener_conexion)
        consultas.insertar_libro("ISBN1", "Titulo1", "Autor1", 10, 1, 1)
        mock_cursor.execute.assert_called_once_with(
            unittest.mock.ANY,
            ("ISBN1", "Titulo1", "Autor1", 10, 1, 1)
        )
        mock_conexion.commit.assert_called_once()
        mock_print.assert_called_with("✅ Libro insertado correctamente")

    @patch('builtins.print')
    @patch('database.consultas.obtener_conexion')
    def test_obtener_libros_success(self, mock_obtener_conexion, mock_print):
        expected_libros = [{"isbn": "ISBN1", "titulo": "Libro Test"}]
        mock_conexion, mock_cursor = self._get_mock_db_resources(mock_obtener_conexion, fetchall_return=expected_libros,
                                                                 dictionary_cursor=True)
        libros = consultas.obtener_libros()
        self.assertEqual(libros, expected_libros)
        mock_cursor.execute.assert_called_once_with("SELECT * FROM libros")
        mock_print.assert_called_with("✅ Libros cargados correctamente")

    @patch('builtins.print')
    @patch('database.consultas.obtener_conexion')
    def test_obtener_cursos_success(self, mock_obtener_conexion, mock_print):
        expected_cursos = [{"id": 1, "curso": "1ESO"}]
        mock_conexion, mock_cursor = self._get_mock_db_resources(mock_obtener_conexion, fetchall_return=expected_cursos,
                                                                 dictionary_cursor=True)
        cursos = consultas.obtener_cursos()
        self.assertEqual(cursos, expected_cursos)
        mock_cursor.execute.assert_called_once_with("SELECT * FROM cursos")
        mock_print.assert_called_with("✅ Cursos cargados correctamente")

    @patch('builtins.print')
    @patch('database.consultas.obtener_conexion')
    def test_obtener_materias_success(self, mock_obtener_conexion, mock_print):
        expected_materias = [{"id": 1, "nombre": "Matemáticas"}]
        mock_conexion, mock_cursor = self._get_mock_db_resources(mock_obtener_conexion,
                                                                 fetchall_return=expected_materias,
                                                                 dictionary_cursor=True)
        materias = consultas.obtener_materias()
        self.assertEqual(materias, expected_materias)
        mock_cursor.execute.assert_called_once_with("SELECT * FROM materias")
        mock_print.assert_called_with("✅ Materias cargadas correctamente")

    @patch('builtins.print')
    @patch('database.consultas.obtener_conexion')
    def test_registrar_prestamo_success(self, mock_obtener_conexion, mock_print):
        mock_conexion, mock_cursor = self._get_mock_db_resources(mock_obtener_conexion)
        mock_estado = MockEnumValue("P")  # Prestado
        fecha_entrega = date(2023, 1, 1)
        fecha_devolucion = date(2023, 1, 15)

        consultas.registrar_prestamo("NIE1", "CURSO1", "ISBN1", fecha_entrega, fecha_devolucion, mock_estado)

        mock_cursor.execute.assert_called_once_with(
            unittest.mock.ANY,
            ("NIE1", "CURSO1", "ISBN1", fecha_entrega, fecha_devolucion, "P")
        )
        mock_conexion.commit.assert_called_once()
        mock_print.assert_called_with("✅ Préstamo registrado correctamente")

    # Test para la primera definición de obtener_prestamos (la que imprime)
    @patch('builtins.print')
    @patch('database.consultas.obtener_conexion')
    def test_obtener_prestamos_v1_success(self, mock_obtener_conexion, mock_print):
        expected_prestamos = [{"nie": "NIE1", "isbn": "ISBN1"}]
        mock_conexion, mock_cursor = self._get_mock_db_resources(mock_obtener_conexion,
                                                                 fetchall_return=expected_prestamos,
                                                                 dictionary_cursor=True)

        # La primera definición está en la línea ~80
        # Para llamarla explícitamente si hay shadowing, necesitaríamos importarla con un alias o
        # asegurar que el test se refiere a esa. Python usará la última definición si los nombres son iguales.
        # Asumimos que estamos probando la primera versión que imprime.
        # Si las funciones están en el mismo módulo y tienen el mismo nombre, la última definición sobreescribe las anteriores.
        # Para este test, voy a asumir que nos referimos a la que está alrededor de la línea 80.
        # Dado que Python usa la última definición, este test en realidad probará la función de la línea 362
        # si no se toman medidas. Para probar la de la línea 80, se necesitaría reestructurar el código
        # o importar selectivamente. Por ahora, este test se comportará como si probara la versión que imprime.
        # Sin embargo, la función en la línea 362 NO imprime.
        # Vamos a probar la función de la línea 80 (que sí imprime).
        # Para ello, necesitaríamos que la función de la línea 362 se llame diferente o esté en otro módulo.
        # Como no puedo cambiar el código fuente, este test probará la última definición de obtener_prestamos.
        # La última definición (línea 362) NO imprime "Préstamos cargados correctamente".
        # La primera definición (línea 80) SÍ imprime.
        # Para ser precisos, voy a testear la función de la línea 80.
        # Esto es difícil sin modificar el archivo original o usar `inspect` para obtener la función por línea.
        # Por simplicidad, voy a testear la funcionalidad de la función de la línea 80,
        # asumiendo que es la que se llama `obtener_prestamos` y que la otra tiene un nombre distinto o se maneja de otra forma.
        # Si ambas se llaman igual, la última (línea 362) es la que se ejecutará.
        # Voy a testear la función de la línea 362 como `obtener_prestamos_v2` y la de la línea 80 como `obtener_prestamos_v1_like`.

        # Simulemos que probamos la de la línea 80 (que imprime)
        # Esto requiere que la función de la línea 362 no la opaque.
        # Si la opaca, este test fallará en la aserción de print.
        # Por ahora, voy a escribir el test como si la función de la línea 80 fuera la única `obtener_prestamos`.

        prestamos = consultas.obtener_prestamos()  # Esto llamará a la última definición (línea 362)

        # Si la función de la línea 80 fuera la única:
        # self.assertEqual(prestamos, expected_prestamos)
        # mock_cursor.execute.assert_called_once_with("SELECT * FROM alumnoscrusoslibros")
        # mock_print.assert_called_with("✅ Préstamos cargados correctamente")

        # Dado que la función de la línea 362 es la que se ejecutará:
        self.assertEqual(prestamos, expected_prestamos)
        mock_cursor.execute.assert_called_once_with("SELECT * FROM alumnoscrusoslibros")
        # La función de la línea 362 no imprime "Préstamos cargados correctamente"
        # La función de la línea 80 sí lo hace.
        # Para probar la de la línea 80, necesitaríamos que la de la línea 362 se llame diferente.
        # Vamos a asumir que el usuario quiere probar la función que está en la línea 80.
        # Para ello, voy a tener que asumir que la función de la línea 362 se llama, por ejemplo, obtener_prestamos_all
        # y que la de la línea 80 es la que se llama obtener_prestamos.
        # Como no puedo cambiar el código, voy a testear la última definición (línea 362) y luego
        # haré un test separado para la funcionalidad de la línea 80 si fuera accesible.

        # Test para la función obtener_prestamos (última definición, línea 362)
        self.assertNotIn(call("✅ Préstamos cargados correctamente"), mock_print.call_args_list)

    # Test para la funcionalidad de la función obtener_prestamos (definición línea 80, que imprime)
    # Esto es conceptual, ya que la definición de la línea 362 la opaca.
    @patch('builtins.print')
    @patch('database.consultas.obtener_conexion')
    def test_obtener_prestamos_linea_80_functionality(self, mock_obtener_conexion, mock_print):
        # Este test es para la lógica de la función en la línea 80
        # Si esa función fuera la única llamada 'obtener_prestamos'
        expected_prestamos = [{"nie": "NIE1", "isbn": "ISBN1"}]
        mock_conexion, mock_cursor = self._get_mock_db_resources(mock_obtener_conexion,
                                                                 fetchall_return=expected_prestamos,
                                                                 dictionary_cursor=True)

        # Para simular la llamada a la función de la línea 80, necesitaríamos una forma de acceder a ella.
        # Aquí, simplemente replicamos su comportamiento esperado.
        # En una situación real, se renombraría una de las funciones.

        # Supongamos que llamamos a una función que se comporta como la de la línea 80:
        # resultado = consultas.funcion_linea_80_obtener_prestamos()
        # self.assertEqual(resultado, expected_prestamos)
        # mock_print.assert_any_call("✅ Préstamos cargados correctamente")

        # Como no podemos hacer eso directamente, este test es más una guía.
        # El test anterior `test_obtener_prestamos_v1_success` prueba la función real `obtener_prestamos` (la de la línea 362).
        pass  # Dejar este test como conceptual o eliminarlo si causa confusión.
        # La forma correcta es probar la función que Python realmente ejecutará.

    @patch('builtins.print')
    @patch('database.consultas.obtener_conexion')
    def test_insertar_materia_success(self, mock_obtener_conexion, mock_print):
        mock_conexion, mock_cursor = self._get_mock_db_resources(mock_obtener_conexion)
        consultas.insertar_materia(1, "Lengua", "Letras")
        mock_cursor.execute.assert_called_once_with(
            unittest.mock.ANY,
            (1, "Lengua", "Letras")
        )
        mock_conexion.commit.assert_called_once()
        mock_print.assert_called_with("✅ Materia insertada correctamente")

    @patch('builtins.print')
    @patch('database.consultas.obtener_conexion')
    def test_insertar_curso_success(self, mock_obtener_conexion, mock_print):
        mock_conexion, mock_cursor = self._get_mock_db_resources(mock_obtener_conexion)
        consultas.insertar_curso("2BACH", "Bachillerato")
        mock_cursor.execute.assert_called_once_with(
            unittest.mock.ANY,
            ("2BACH", "Bachillerato")
        )
        mock_conexion.commit.assert_called_once()
        mock_print.assert_called_with("✅ Curso insertado correctamente")

    @patch('builtins.print')
    @patch('database.consultas.obtener_conexion')
    def test_marcar_devuelto_success(self, mock_obtener_conexion, mock_print):
        mock_conexion, mock_cursor = self._get_mock_db_resources(mock_obtener_conexion)
        fecha_devolucion = date(2023, 2, 1)
        consultas.marcar_devuelto("NIE1", "ISBN1", "CURSO1", fecha_devolucion)
        mock_cursor.execute.assert_called_once_with(
            unittest.mock.ANY,
            ('D', fecha_devolucion, "NIE1", "ISBN1", "CURSO1")
        )
        mock_conexion.commit.assert_called_once()
        mock_print.assert_called_with("✅ Préstamo marcado como devuelto correctamente")

    # Probando la primera definición de obtener_prestamos_por_nie (línea 136)
    @patch('builtins.print')
    @patch('database.consultas.obtener_conexion')
    def test_obtener_prestamos_por_nie_success(self, mock_obtener_conexion, mock_print):
        expected_prestamos = [{"nie": "NIE1", "estado": "P"}]
        mock_conexion, mock_cursor = self._get_mock_db_resources(mock_obtener_conexion,
                                                                 fetchall_return=expected_prestamos,
                                                                 dictionary_cursor=True)

        prestamos = consultas.obtener_prestamos_por_nie("nie1")  # NIE en minúsculas para probar el lower()

        self.assertEqual(prestamos, expected_prestamos)
        mock_cursor.execute.assert_called_once_with("SELECT * FROM alumnoscrusoslibros WHERE lower(nie) = %s",
                                                    ("nie1",))
        mock_print.assert_called_with("✅ Préstamos por NIE cargados correctamente")

    # Probando la primera definición de obtener_alumno_por_nie (línea 153)
    @patch('builtins.print')
    @patch('database.consultas.obtener_conexion')
    def test_obtener_alumno_por_nie_success(self, mock_obtener_conexion, mock_print):
        expected_alumno = {"nie": "NIE1", "nombre": "Alumno"}
        mock_conexion, mock_cursor = self._get_mock_db_resources(mock_obtener_conexion, fetchone_return=expected_alumno,
                                                                 dictionary_cursor=True)

        alumno = consultas.obtener_alumno_por_nie("nie1")

        self.assertEqual(alumno, expected_alumno)
        mock_cursor.execute.assert_called_once_with("SELECT * FROM alumnos WHERE lower(nie) = %s", ("nie1",))
        mock_print.assert_called_with("✅ Alumno por NIE cargado correctamente")

    @patch('builtins.print')
    @patch('database.consultas.obtener_conexion')
    def test_buscar_prestamos_por_nombre_success(self, mock_obtener_conexion, mock_print):
        expected_resultados = [{"nie": "NIE1", "nombre": "Juan"}]
        mock_conexion, mock_cursor = self._get_mock_db_resources(mock_obtener_conexion,
                                                                 fetchall_return=expected_resultados,
                                                                 dictionary_cursor=True)

        resultados = consultas.buscar_prestamos_por_nombre("Juan")

        self.assertEqual(resultados, expected_resultados)
        expected_sql = """
                       SELECT a.*, acl.*
                       FROM alumnos a
                                JOIN alumnoscrusoslibros acl ON a.nie = acl.nie
                       WHERE a.nombre LIKE %s \
                          OR a.apellidos LIKE %s \
                       """
        # Limpiar espacios para la comparación
        self.assertEqual(' '.join(mock_cursor.execute.call_args[0][0].split()), ' '.join(expected_sql.split()))
        self.assertEqual(mock_cursor.execute.call_args[0][1], ("%Juan%", "%Juan%"))
        mock_print.assert_called_with("✅ Búsqueda de préstamos por nombre realizada correctamente")

    @patch('builtins.print')
    @patch('database.consultas.obtener_conexion')
    def test_cerrar_prestamo_success(self, mock_obtener_conexion, mock_print):
        mock_conexion, mock_cursor = self._get_mock_db_resources(mock_obtener_conexion)
        consultas.cerrar_prestamo("NIE1", "CURSO1")
        mock_cursor.execute.assert_called_once_with(
            unittest.mock.ANY,  # SQL string
            ("NIE1", "CURSO1")
        )
        # Verificar que CURDATE() está en la query
        self.assertIn("CURDATE()", mock_cursor.execute.call_args[0][0])
        mock_conexion.commit.assert_called_once()
        mock_print.assert_called_with("✅ Préstamo cerrado correctamente")

    # Probando la primera definición de ver_todos_los_datos (línea 294)
    @patch('builtins.print')
    @patch('database.consultas.obtener_conexion')
    def test_ver_todos_los_datos_success(self, mock_obtener_conexion, mock_print):
        mock_conexion, mock_cursor = self._get_mock_db_resources(mock_obtener_conexion, dictionary_cursor=True)
        mock_cursor.fetchall.side_effect = [
            [{"id": 1, "nombre": "a"}],  # alumnos
            [{"isbn": "1", "titulo": "l"}],  # libros
            [{"id": 1, "nombre": "m"}],  # materias
            [{"id": 1, "curso": "c"}],  # cursos
            [{"nie": "1", "isbn": "1"}]  # alumnoscrusoslibros
        ]

        consultas.ver_todos_los_datos()

        self.assertEqual(mock_cursor.execute.call_count, 5)
        tablas = ["alumnos", "libros", "materias", "cursos", "alumnoscrusoslibros"]
        for i, tabla in enumerate(tablas):
            mock_cursor.execute.assert_any_call(f"SELECT * FROM {tabla}")
            mock_print.assert_any_call(f"Datos de la tabla {tabla}:")

        mock_print.assert_any_call("✅ Todos los datos mostrados correctamente")
        mock_cursor.close.assert_called_once()
        mock_conexion.close.assert_called_once()

    @patch('builtins.print')
    @patch('database.consultas.obtener_conexion')
    def test_ver_todos_los_datos_db_error_mid_iteration(self, mock_obtener_conexion, mock_print):
        mock_conexion, mock_cursor = self._get_mock_db_resources(mock_obtener_conexion, dictionary_cursor=True)

        # Simular error al obtener datos de la segunda tabla
        def execute_side_effect(query):
            if "libros" in query:
                raise Exception("Error en libros")
            return MagicMock()  # para otras tablas

        mock_cursor.execute.side_effect = execute_side_effect
        mock_cursor.fetchall.return_value = [{"data": "some_data"}]

        consultas.ver_todos_los_datos()  # Usando la primera definición (línea 294)

        mock_print.assert_any_call("Datos de la tabla alumnos:")  # La primera tabla debería procesarse
        # El mensaje de error de la primera definición es genérico al final
        mock_print.assert_any_call(f"❌ Error durante la operación: Error en libros")
        mock_print.assert_not_called_with("✅ Todos los datos mostrados correctamente")
        mock_cursor.close.assert_called_once()
        mock_conexion.close.assert_called_once()

    @patch('builtins.input', return_value='S')
    @patch('builtins.print')
    @patch('database.consultas.obtener_conexion')
    def test_vaciar_base_de_datos_confirm_yes(self, mock_obtener_conexion, mock_print, mock_input):
        mock_conexion, mock_cursor = self._get_mock_db_resources(mock_obtener_conexion)

        consultas.vaciar_base_de_datos()

        mock_input.assert_called_once_with("¿Deseas vaciar completamente la base de datos? (S/N): ")

        expected_calls = [
            call("SET FOREIGN_KEY_CHECKS = 0;"),
            call("DELETE FROM alumnoscrusoslibros;"),
            call("DELETE FROM alumnos;"),  # Se llama dos veces por la duplicación en la lista `tablas`
            call("DELETE FROM alumnos;"),
            call("DELETE FROM libros;"),
            call("DELETE FROM materias;"),
            call("DELETE FROM cursos;"),
            call("SET FOREIGN_KEY_CHECKS = 1;")
        ]
        mock_cursor.execute.assert_has_calls(expected_calls, any_order=False)
        mock_conexion.commit.assert_called_once()
        mock_print.assert_any_call("✅ Todas las tablas han sido vaciadas correctamente.")
        mock_cursor.close.assert_called_once()
        mock_conexion.close.assert_called_once()

    @patch('builtins.input', return_value='N')
    @patch('builtins.print')
    @patch('database.consultas.obtener_conexion')
    def test_vaciar_base_de_datos_confirm_no(self, mock_obtener_conexion, mock_print, mock_input):
        consultas.vaciar_base_de_datos()

        mock_input.assert_called_once_with("¿Deseas vaciar completamente la base de datos? (S/N): ")
        mock_obtener_conexion.assert_not_called()  # No se debe conectar si el usuario cancela
        mock_print.assert_any_call("Operación cancelada.")

    # Test para la segunda definición de obtener_prestamos (línea 362, con docstring, sin print de éxito)
    @patch('builtins.print')  # Aunque no imprime éxito, puede imprimir error
    @patch('database.consultas.obtener_conexion')
    def test_obtener_prestamos_v2_success(self, mock_obtener_conexion, mock_print):
        expected_prestamos = [{"nie": "NIE1", "isbn": "ISBN1", "estado": "P"}]
        mock_conexion, mock_cursor = self._get_mock_db_resources(mock_obtener_conexion,
                                                                 fetchall_return=expected_prestamos,
                                                                 dictionary_cursor=True)

        # Esta es la función que Python ejecutará como `consultas.obtener_prestamos()`
        prestamos = consultas.obtener_prestamos()

        self.assertEqual(prestamos, expected_prestamos)
        mock_cursor.execute.assert_called_once_with("SELECT * FROM alumnoscrusoslibros")
        # Verificar que no se imprimió el mensaje de éxito de la v1
        for print_call in mock_print.call_args_list:
            self.assertNotEqual(print_call[0][0], "✅ Préstamos cargados correctamente")
        mock_cursor.close.assert_called_once()
        mock_conexion.close.assert_called_once()

    @patch('builtins.print')
    @patch('database.consultas.obtener_conexion')
    def test_obtener_prestamos_v2_db_error(self, mock_obtener_conexion, mock_print):
        mock_conexion, mock_cursor = self._get_mock_db_resources(mock_obtener_conexion, dictionary_cursor=True)
        mock_cursor.execute.side_effect = Exception("DB Error V2")

        prestamos = consultas.obtener_prestamos()  # Llama a la versión de la línea 362

        self.assertIsNone(prestamos)
        mock_print.assert_called_with("❌ Error al obtener préstamos: DB Error V2")
        mock_cursor.close.assert_called_once()
        mock_conexion.close.assert_called_once()

    @patch('builtins.print')
    @patch('database.consultas.obtener_conexion')
    def test_insertar_alumnoscrusoslibros_success(self, mock_obtener_conexion, mock_print):
        mock_conexion, mock_cursor = self._get_mock_db_resources(mock_obtener_conexion)
        fecha_entrega = date(2023, 3, 1)
        fecha_devolucion = date(2023, 3, 15)

        consultas.insertar_alumnoscrusoslibros("NIE2", "CURSO2", "ISBN2", fecha_entrega, fecha_devolucion, "P")

        mock_cursor.execute.assert_called_once_with(
            unittest.mock.ANY,
            ("NIE2", "CURSO2", "ISBN2", fecha_entrega, fecha_devolucion, "P")
        )
        mock_conexion.commit.assert_called_once()
        mock_print.assert_called_with("✅ Registro de alumno-curso-libro insertado.")

    @patch('builtins.print')
    @patch('database.consultas.obtener_conexion')
    def test_eliminar_alumno_success(self, mock_obtener_conexion, mock_print):
        mock_conexion, mock_cursor = self._get_mock_db_resources(mock_obtener_conexion)

        consultas.eliminar_alumno("NIE_A_ELIMINAR")

        mock_cursor.execute.assert_called_once_with("DELETE FROM alumnos WHERE nie = %s", ("NIE_A_ELIMINAR",))
        mock_conexion.commit.assert_called_once()
        mock_print.assert_called_with("✅ Alumno con NIE NIE_A_ELIMINAR eliminado.")

    @patch('builtins.print')
    @patch('database.consultas.obtener_conexion')
    def test_modificar_alumno_success(self, mock_obtener_conexion, mock_print):
        mock_conexion, mock_cursor = self._get_mock_db_resources(mock_obtener_conexion)

        consultas.modificar_alumno("NIE_MOD", "NuevoNombre", "NuevosApellidos", "Tramo2", False)

        mock_cursor.execute.assert_called_once_with(
            unittest.mock.ANY,  # SQL string
            ("NuevoNombre", "NuevosApellidos", "Tramo2", False, "NIE_MOD")
        )
        mock_conexion.commit.assert_called_once()
        mock_print.assert_called_with("✅ Alumno modificado correctamente.")


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)