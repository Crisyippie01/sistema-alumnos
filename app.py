"""!
@file app.py
@brief API de gestión de alumnos "Sistema Alumnos" (actividad OCY1102).
"""
import os

from flask import Flask, jsonify, request

## @brief Instancia principal de la app Flask
app = Flask(__name__)

## @brief  Base de datos en memoria (solo para fines de la actividad)
ALUMNOS = [
    {"id": 1, "nombre": "Ana Pérez", "carrera": "Ingeniería en Informática", "promedio": 6.1},
    {"id": 2, "nombre": "Benjamín Rojas", "carrera": "Ingeniería en Ciberseguridad", "promedio": 5.4},
    {"id": 3, "nombre": "Camila Soto", "carrera": "Analista Programador", "promedio": 6.8},
]

## @var VERSION
#  @brief version actual de la app (por defecto "dev").
VERSION = os.environ.get("APP_VERSION", "dev")


@app.route('/hello')
def hello():
    """
    @brief Endpoint para saludar al usuario.
    @return str: Mensaje de saludo.
    """
    name = request.args.get('name')
    return f"Hello, {name}!"


@app.route('/health')
def health():
    """
    @brief Endpoint para verificar estado 
    @return JSON con el estado de la API
     """
    return jsonify({"estado": "ok"})


@app.route('/version')
def version():
    """!
    @brief Endpoint para obtener la version actual de la app.
    @return JSON con el nombre de la app y la version.
    """
    return jsonify({"aplicacion": "Sistema Alumnos", "version": VERSION})


@app.route('/alumnos')
def listar_alumnos():
    """!
    @brief Endpoint para obtener la lista de alumnos.
    @return JSON con la lista de todos los alumnos registrados.
    """
    return jsonify(ALUMNOS)


@app.route('/alumnos/<int:alumno_id>')
def obtener_alumno(alumno_id):
    """!
    @brief Endpoint para obtener los datos de un alumno por su ID.
    
    @param alumno_id ID unico del alumno a buscar.
    @return JSON con los datos del alumno si es encontrado o 404 si no existe.
    """
    for alumno in ALUMNOS:
        if alumno["id"] == alumno_id:
            return jsonify(alumno)
    return jsonify({"error": "Alumno no encontrado"}), 404


@app.route('/alumnos', methods=['POST'])
def crear_alumno():
    """!
    @brief Endpoint para crear un nuevo registro de alumno.
    @return JSON con los datos del alumno recien creado, o 400 si los datos son invalidos.
    """
    datos = request.get_json(silent=True) or {}
    nombre = str(datos.get("nombre", "")).strip()
    promedio = datos.get("promedio")

    if not nombre:
        return jsonify({"error": "El campo 'nombre' es obligatorio"}), 400
    if not isinstance(promedio, (int, float)) or not 1.0 <= promedio <= 7.0:
        return jsonify({"error": "El 'promedio' debe ser un número entre 1.0 y 7.0"}), 400

    nuevo = {
        "id": max(a["id"] for a in ALUMNOS) + 1,
        "nombre": nombre,
        "carrera": str(datos.get("carrera", "Sin carrera")),
        "promedio": promedio,
    }
    ALUMNOS.append(nuevo)
    return jsonify(nuevo), 201


if __name__ == '__main__':
    ## @brief Bloque principal de ejecución para iniciar el servidor.
    app.run(debug=True)
