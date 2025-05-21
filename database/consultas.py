from database.conexion import obtener_conexion

def insertar_alumno(nie, nombre, apellidos, tramo, bilingue):
    conexion = obtener_conexion()
    if not conexion:
        return
    cursor = conexion.cursor()
    try:
        cursor.execute("""
            INSERT INTO alumnos (nie, nombre, apellidos, tramo, bilingue)
            VALUES (%s, %s, %s, %s, %s)
        """, (nie, nombre, apellidos, tramo.value, bilingue))
        conexion.commit()
    except Exception as e:
        print(f"❌ Error durante la operación: {e}")
    finally:
        cursor.close()
        conexion.close()

def obtener_alumnos():
    conexion = obtener_conexion()
    if not conexion:
        return
    cursor = conexion.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM alumnos")
        alumnos = cursor.fetchall()
        return alumnos
    except Exception as e:
        print(f"❌ Error durante la operación: {e}")
    finally:
        cursor.close()
        conexion.close()

def insertar_libro(isbn, titulo, autor, ejemplares, id_materia, id_curso):
    conexion = obtener_conexion()
    if not conexion:
        return
    cursor = conexion.cursor()
    try:
        cursor.execute("""
            INSERT INTO libros (isbn, titulo, autor, numero_ejemplares, id_materia, id_curso)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (isbn, titulo, autor, ejemplares, id_materia, id_curso))
        conexion.commit()
    except Exception as e:
        print(f"❌ Error durante la operación: {e}")
    finally:
        cursor.close()
        conexion.close()

def obtener_libros():
    conexion = obtener_conexion()
    if not conexion:
        return
    cursor = conexion.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM libros")
        libros = cursor.fetchall()
        return libros
    except Exception as e:
        print(f"❌ Error durante la operación: {e}")
    finally:
        cursor.close()
        conexion.close()

def obtener_cursos():
    conexion = obtener_conexion()
    if not conexion:
        return
    cursor = conexion.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM cursos")
        cursos = cursor.fetchall()
        return cursos
    except Exception as e:
        print(f"❌ Error durante la operación: {e}")
    finally:
        cursor.close()
        conexion.close()

def obtener_materias():
    conexion = obtener_conexion()
    if not conexion:
        return
    cursor = conexion.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM materias")
        materias = cursor.fetchall()
        return materias
    except Exception as e:
        print(f"❌ Error durante la operación: {e}")
    finally:
        cursor.close()
        conexion.close()

def registrar_prestamo(nie, curso, isbn, fecha_entrega, fecha_devolucion, estado):
    conexion = obtener_conexion()
    if not conexion:
        return
    cursor = conexion.cursor(dictionary=True)

    try:
        cursor.execute("SELECT numero_ejemplares FROM libros WHERE isbn = %s", (isbn,))
        resultado = cursor.fetchone()

        if not resultado:
            print("❌ Libro no encontrado.")
            return

        ejemplares = resultado["numero_ejemplares"]
        if ejemplares <= 0:
            print("❌ No se puede prestar este libro. No hay ejemplares disponibles.")
            return

        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO alumnoscrusoslibros 
            (nie, curso, isbn, fecha_entrega, fecha_devolucion, estado)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (nie, curso, isbn, fecha_entrega, fecha_devolucion, estado.value))

        cursor.execute("""
            UPDATE libros SET numero_ejemplares = numero_ejemplares - 1
            WHERE isbn = %s
        """, (isbn,))

        conexion.commit()
        print("✅ Préstamo registrado correctamente")

    except Exception as e:
        print(f"❌ Error durante la operación: {e}")
    finally:
        cursor.close()
        conexion.close()

def obtener_prestamos():
    conexion = obtener_conexion()
    if not conexion:
        return
    cursor = conexion.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM alumnoscrusoslibros")
        prestamos = cursor.fetchall()
        return prestamos
    except Exception as e:
        print(f"❌ Error durante la operación: {e}")
    finally:
        cursor.close()
        conexion.close()

def insertar_materia(id, nombre, departamento):
    conexion = obtener_conexion()
    if not conexion:
        return
    cursor = conexion.cursor()
    try:
        cursor.execute("""
            INSERT INTO materias (id, nombre, departamento)
            VALUES (%s, %s, %s)
        """, (id, nombre, departamento))
        conexion.commit()
    except Exception as e:
        print(f"❌ Error durante la operación: {e}")
    finally:
        cursor.close()
        conexion.close()

def insertar_curso(curso, nivel):
    conexion = obtener_conexion()
    if not conexion:
        return
    cursor = conexion.cursor()
    try:
        cursor.execute("""
            INSERT INTO cursos (curso, nivel)
            VALUES (%s, %s)
        """, (curso, nivel))
        conexion.commit()
    except Exception as e:
        print(f"❌ Error durante la operación: {e}")
    finally:
        cursor.close()
        conexion.close()

def marcar_devuelto(nie, isbn, curso, fecha_devolucion):
    conexion = obtener_conexion()
    if not conexion:
        return
    cursor = conexion.cursor()
    try:
        cursor.execute("""
            UPDATE alumnoscrusoslibros
            SET estado = %s, fecha_devolucion = %s
            WHERE lower(nie) = %s AND lower(isbn) = %s AND lower(curso) = %s
        """, ('D', fecha_devolucion, nie, isbn, curso))
        conexion.commit()
    except Exception as e:
        print(f"❌ Error durante la operación: {e}")
    finally:
        cursor.close()
        conexion.close()

def obtener_prestamos_por_nie(nie):
    conexion = obtener_conexion()
    if not conexion:
        return
    cursor = conexion.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM alumnoscrusoslibros WHERE lower(nie) = %s", (nie,))
        prestamos = cursor.fetchall()
        return prestamos
    except Exception as e:
        print(f"❌ Error durante la operación: {e}")
    finally:
        cursor.close()
        conexion.close()

def obtener_alumno_por_nie(nie):
    conexion = obtener_conexion()
    if not conexion:
        return
    cursor = conexion.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM alumnos WHERE lower(nie) = %s", (nie,))
        alumno = cursor.fetchone()
        return alumno
    except Exception as e:
        print(f"❌ Error durante la operación: {e}")
    finally:
        cursor.close()
        conexion.close()

def buscar_prestamos_por_nie(nie):
    conexion = obtener_conexion()
    if not conexion:
        return
    cursor = conexion.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM alumnoscrusoslibros WHERE lower(nie) = %s", (nie,))
        resultados = cursor.fetchall()
        return resultados
    except Exception as e:
        print(f"❌ Error durante la operación: {e}")
    finally:
        cursor.close()
        conexion.close()

def buscar_prestamos_por_nombre(nombre):
    conexion = obtener_conexion()
    if not conexion:
        return
    cursor = conexion.cursor(dictionary=True)
    try:
        sql = """
        SELECT a.*, acl.*
        FROM alumnos a
        JOIN alumnoscrusoslibros acl ON a.nie = acl.nie
        WHERE a.nombre LIKE %s OR a.apellidos LIKE %s
        """
        like_nombre = f"%{nombre}%"
        cursor.execute(sql, (like_nombre, like_nombre))
        resultados = cursor.fetchall()
        return resultados
    except Exception as e:
        print(f"❌ Error durante la operación: {e}")
    finally:
        cursor.close()
        conexion.close()

def buscar_prestamos_por_curso(curso):
    conexion = obtener_conexion()
    if not conexion:
        return
    cursor = conexion.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM alumnoscrusoslibros WHERE lower(curso) = %s", (curso,))
        resultados = cursor.fetchall()
        return resultados
    except Exception as e:
        print(f"❌ Error durante la operación: {e}")
    finally:
        cursor.close()
        conexion.close()

def buscar_prestamos_por_isbn(isbn):
    conexion = obtener_conexion()
    if not conexion:
        return
    cursor = conexion.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM alumnoscrusoslibros WHERE lower(isbn) = %s", (isbn,))
        resultados = cursor.fetchall()
        return resultados
    except Exception as e:
        print(f"❌ Error durante la operación: {e}")
    finally:
        cursor.close()
        conexion.close()

def buscar_prestamos_por_estado(estado):
    conexion = obtener_conexion()
    if not conexion:
        return
    cursor = conexion.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM alumnoscrusoslibros WHERE upper(estado) = %s", (estado,))
        resultados = cursor.fetchall()
        return resultados
    except Exception as e:
        print(f"❌ Error durante la operación: {e}")
    finally:
        cursor.close()
        conexion.close()

def cerrar_prestamo(nie, curso):
    conexion = obtener_conexion()
    if not conexion:
        return
    cursor = conexion.cursor()
    try:
        cursor.execute("""
            UPDATE alumnoscrusoslibros
            SET estado = 'D', fecha_devolucion = CURDATE()
            WHERE nie = %s AND curso = %s AND estado = 'P'
        """, (nie, curso))
        conexion.commit()
    except Exception as e:
        print(f"❌ Error durante la operación: {e}")
    finally:
        cursor.close()
        conexion.close()

def obtener_alumnoscrusoslibros():
    conexion = obtener_conexion()
    if not conexion:
        return
    cursor = conexion.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM alumnoscrusoslibros")
        datos = cursor.fetchall()
        return datos
    except Exception as e:
        print(f"❌ Error durante la operación: {e}")
    finally:
        cursor.close()
        conexion.close()

def ver_todos_los_datos():
    conexion = obtener_conexion()
    if not conexion:
        return
    tablas = ["alumnos", "libros", "materias", "cursos", "alumnoscrusoslibros"]
    cursor = conexion.cursor(dictionary=True)
    try:
        for tabla in tablas:
            cursor.execute(f"SELECT * FROM {tabla}")
            datos = cursor.fetchall()
            print(f"Datos de la tabla {tabla}:")
            for fila in datos:
                print(fila)
            print("\n")
    except Exception as e:
        print(f"❌ Error durante la operación: {e}")
    finally:
        cursor.close()
        conexion.close()

def vaciar_base_de_datos():
    """
    Vacia completamente todas las tablas de la base de datos.
    """
    print("--- VACIAR BASE DE DATOS ---")
    confirmar = input("¿Deseas vaciar completamente la base de datos? (S/N): ").strip().upper()
    if confirmar != 'S':
        print("Operación cancelada.")
        return

    tablas = [
        "alumnoscrusoslibros",
        "alumnos",
        "alumnos",
        "libros",
        "materias",
        "cursos"
    ]

    conexion = obtener_conexion()
    if not conexion:
        return

    cursor = conexion.cursor()
    try:
        for tabla in tablas:
            cursor.execute(f"DELETE FROM {tabla};")
        conexion.commit()
    except Exception as e:
        print(f"❌ Error al vaciar la base de datos: {e}")
    finally:
        cursor.close()
        conexion.close()

def insertar_alumnoscrusoslibros(nie, curso, isbn, fecha_entrega, fecha_devolucion, estado):
    conexion = obtener_conexion()
    if not conexion:
        return
    cursor = conexion.cursor()
    try:
        cursor.execute("""
            INSERT INTO alumnoscrusoslibros
            (nie, curso, isbn, fecha_entrega, fecha_devolucion, estado)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (nie, curso, isbn, fecha_entrega, fecha_devolucion, estado))
        conexion.commit()
    except Exception as e:
        print(f"❌ Error al insertar alumno-curso-libro: {e}")
    finally:
        cursor.close()
        conexion.close()

def eliminar_alumno(nie):
    conexion = obtener_conexion()
    if not conexion:
        return
    cursor = conexion.cursor()
    try:
        cursor.execute("DELETE FROM alumnos WHERE nie = %s", (nie,))
        conexion.commit()
    except Exception as e:
        print(f"❌ Error al eliminar alumno: {e}")
    finally:
        cursor.close()
        conexion.close()

def modificar_alumno(nie, nombre, apellidos, tramo, bilingue):
    conexion = obtener_conexion()
    if not conexion:
        return
    cursor = conexion.cursor()
    try:
        cursor.execute("""
            UPDATE alumnos
            SET nombre = %s, apellidos = %s, tramo = %s, bilingue = %s
            WHERE nie = %s
        """, (nombre, apellidos, tramo, bilingue, nie))
        conexion.commit()
    except Exception as e:
        print(f"❌ Error al modificar alumno: {e}")
    finally:
        cursor.close()
        conexion.close()