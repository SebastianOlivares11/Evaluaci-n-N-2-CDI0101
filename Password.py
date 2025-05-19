import sqlite3
from flask import Flask, request, jsonify

NOMBRE_BD = "usuarios.db"

def inicializar_bd():
    conexion = sqlite3.connect(NOMBRE_BD)
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            usuario TEXT PRIMARY KEY,
            contrasena TEXT
        )
    ''')
    conexion.commit()
    conexion.close()

def agregar_usuario(usuario, contrasena):
    conexion = sqlite3.connect(NOMBRE_BD)
    cursor = conexion.cursor()
    try:
        cursor.execute('INSERT INTO usuarios (usuario, contrasena) VALUES (?, ?)', (usuario, contrasena))
        conexion.commit()
    except sqlite3.IntegrityError:
        pass  # El usuario ya existe
    conexion.close()

def verificar_usuario(usuario, contrasena):
    conexion = sqlite3.connect(NOMBRE_BD)
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM usuarios WHERE usuario=? AND contrasena=?', (usuario, contrasena))
    usuario_encontrado = cursor.fetchone()
    conexion.close()
    return usuario_encontrado is not None

aplicacion = Flask(__name__)

@aplicacion.route('/', methods=['GET'])
def inicio():
    return "Sistema de Control de Credenciales (Fase 1)"

@aplicacion.route('/registrar', methods=['POST'])
def registrar():
    usuario = request.form.get('usuario')
    contrasena = request.form.get('contrasena')
    if not usuario or not contrasena:
        return jsonify({'estado': 'error', 'mensaje': 'Faltan parámetros'}), 400
    agregar_usuario(usuario, contrasena)
    return jsonify({'estado': 'ok', 'mensaje': 'Usuario registrado'})

@aplicacion.route('/iniciar_sesion', methods=['POST'])
def iniciar_sesion():
    usuario = request.form.get('usuario')
    contrasena = request.form.get('contrasena')
    if verificar_usuario(usuario, contrasena):
        return jsonify({'estado': 'ok', 'mensaje': 'Inicio de sesión exitoso'})
    else:
        return jsonify({'estado': 'error', 'mensaje': 'Credenciales inválidas'}), 401

if __name__ == '__main__':
    inicializar_bd()
    aplicacion.run(port=5000)
