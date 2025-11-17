from flask import Flask, render_template, jsonify, request, session, redirect, url_for
from functools import wraps
import requests
import os
import sys
from dotenv import load_dotenv

# Agregar el directorio services al path para importar
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Importar funciones de tu módulo de base de datos existente
from services import data_base_mongo as db_mongo

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'clave_secreta_cambiar_en_produccion')

SERVICE2_URL = os.getenv('SERVICE2_URL', 'http://127.0.0.1:8002/historial')

# Decorador para requerir login
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login_page'))
        return f(*args, **kwargs)
    return decorated_function

# Decorador para verificar rol
def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user' not in session:
                return redirect(url_for('login_page'))
            if session['user'].get('rol') != role:
                return jsonify({"error": "Acceso denegado"}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# ============= RUTAS DE AUTENTICACIÓN =============

@app.route("/")
def home():
    """Redirige según el estado de sesión"""
    if 'user' in session:
        rol = session['user'].get('rol')
        if rol == 'paciente':
            return redirect(url_for('paciente_dashboard'))
        elif rol == 'medico':
            return redirect(url_for('medico_dashboard'))
    return redirect(url_for('login_page'))

@app.route("/login")
def login_page():
    """Muestra la página de login"""
    return render_template("login.html")

@app.route("/login", methods=['POST'])
def login():
    """Procesa el login usando tu conexión MongoDB existente"""
    data = request.get_json()
    cedula = data.get('cedula')
    password = data.get('password')
    
    if not cedula or not password:
        return jsonify({"success": False, "message": "Faltan datos"}), 400
    
    try:
        # Autenticar usando la función de tu módulo
        usuario = db_mongo.autenticar_usuario(cedula, password)
        
        if usuario:
            # Crear sesión
            session['user'] = {
                'cedula': usuario['cedula'],
                'nombre': usuario['nombre'],
                'rol': usuario['rol'],
                'especialidad': usuario.get('especialidad', '')
            }
            return jsonify({
                "success": True,
                "rol": usuario['rol'],
                "message": "Login exitoso"
            })
        
        return jsonify({"success": False, "message": "Credenciales inválidas"}), 401
        
    except Exception as e:
        print(f"Error en login: {e}")
        return jsonify({"success": False, "message": "Error del servidor"}), 500

@app.route("/registro")
def registro_page():
    """Muestra la página de registro"""
    return render_template("registro.html")

@app.route("/registro", methods=['POST'])
def registro():
    """Procesa el registro de nuevos pacientes"""
    data = request.get_json()
    cedula = data.get('cedula')
    nombre = data.get('nombre')
    apellido = data.get('apellido', '')
    fecha_nacimiento = data.get('fecha_nacimiento', '')
    email = data.get('email')
    telefono = data.get('telefono')
    telegram_user_id = data.get('telegram_user_id', '')
    password = data.get('password')
    
    if not all([cedula, nombre, email, telefono, password]):
        return jsonify({"success": False, "message": "Faltan datos obligatorios"}), 400
    
    try:
        # Verificar si ya existe usando tu función
        if db_mongo.usuario_existe(cedula):
            return jsonify({"success": False, "message": "La cédula ya está registrada"}), 400
        
        # Crear usuario usando tu función con todos los campos
        if db_mongo.crear_usuario(
            cedula=cedula, 
            nombre=nombre, 
            email=email, 
            telefono=telefono, 
            password=password, 
            rol='paciente',
            apellido=apellido,
            fecha_nacimiento=fecha_nacimiento,
            telegram_user_id=telegram_user_id
        ):
            return jsonify({"success": True, "message": "Registro exitoso"})
        else:
            return jsonify({"success": False, "message": "Error al registrar usuario"}), 500
            
    except Exception as e:
        print(f"Error en registro: {e}")
        return jsonify({"success": False, "message": "Error del servidor"}), 500

@app.route("/logout")
def logout():
    """Cierra la sesión"""
    session.pop('user', None)
    return redirect(url_for('login_page'))

# ============= DASHBOARDS =============

@app.route("/paciente/dashboard")
@role_required('paciente')
def paciente_dashboard():
    """Dashboard para pacientes"""
    user = session['user']
    return render_template("paciente_dashboard.html", user=user)

@app.route("/medico/dashboard")
@role_required('medico')
def medico_dashboard():
    """Dashboard para médicos"""
    user = session['user']
    return render_template("medico_dashboard.html", user=user)

# ============= APIs =============

@app.route("/api/data/<cedula>")
@login_required
def get_data(cedula):
    """Obtiene el historial de salud por cédula"""
    try:
        response = requests.get(f"{SERVICE2_URL}/{cedula}")
        if response.status_code == 200:
            return jsonify(response.json())
        elif response.status_code == 404:
            return jsonify({"error": "No se encontró historial para esta cédula"}), 404
        else:
            return jsonify({"error": f"Error al conectar con Service2: {response.status_code}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/pacientes")
@role_required('medico')
def get_pacientes():
    """Lista todos los pacientes (solo para médicos)"""
    try:
        pacientes = db_mongo.obtener_pacientes()
        return jsonify(pacientes)
    except Exception as e:
        print(f"Error al obtener pacientes: {e}")
        return jsonify([])

# ============= PÁGINAS DE ERROR =============

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Ruta no encontrada"}), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify({"error": "Error interno del servidor"}), 500

# ============= INICIALIZACIÓN =============

@app.before_request
def inicializar_db():
    """Inicializa datos de prueba en el primer request"""
    if not hasattr(app, 'db_initialized'):
        db_mongo.inicializar_datos_prueba()
        app.db_initialized = True

if __name__ == "__main__":
    print("🚀 Iniciando servidor Flask...")
    print(f"📊 Usando conexión MongoDB desde services/data_base_mongo.py")
    app.run(debug=True, host='0.0.0.0', port=8080)