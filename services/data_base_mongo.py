from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
from dotenv import load_dotenv

# Intentar cargar .env desde la raíz del proyecto (una carpeta arriba de `services`)
here = os.path.abspath(os.path.dirname(__file__))
project_root = os.path.abspath(os.path.join(here, os.pardir))
dotenv_path = os.path.join(project_root, ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
else:
    # Fallback: intentar cargar desde el cwd
    load_dotenv()

# Leer variables de entorno
# Si no hay MONGO_URI, conectamos al localhost por defecto
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME")

try:
    client = MongoClient(MONGO_URI)

    if DB_NAME:
        # Usar la DB especificada por la variable de entorno
        db = client[DB_NAME]
    else:
        # Intentar obtener la base de datos por defecto del URI (si existe)
        db = client.get_default_database()
        if db is None:
            # No hay DB configurada; no intentar indexar con None
            print("⚠️ DB_NAME no configurada y URI no contiene una base de datos por defecto. db será None.")

    if db is not None:
        print("✅ Conectado a MongoDB correctamente crack")
        
        # Crear índices únicos para las colecciones de usuarios
        try:
            db.usuarios.create_index('cedula', unique=True)
            db.pacientes.create_index('cedula', unique=True)
        except:
            pass  # Los índices ya existen
    else:
        print("⚠️ No hay conexión activa con MongoDB (db is None)")

except Exception as e:
    print("❌ Error al conectar con MongoDB:", e)
    db = None


# ============= FUNCIONES PARA GESTIÓN DE USUARIOS =============

def crear_usuario(cedula, nombre, email, telefono, password, rol='paciente', especialidad=None, apellido='', fecha_nacimiento='', telegram_user_id=''):
    """Crea un nuevo usuario en la base de datos"""
    if db is None:
        return False
    
    try:
        # Crear usuario en la colección de usuarios
        usuario = {
            'cedula': cedula,
            'nombre': nombre,
            'email': email,
            'telefono': telefono,
            'password': generate_password_hash(password),
            'rol': rol,
            'fecha_registro': datetime.now(),
            'activo': True
        }
        
        if rol == 'medico' and especialidad:
            usuario['especialidad'] = especialidad
        
        db.usuarios.insert_one(usuario)
        
        # Si es paciente, agregarlo a la colección de pacientes con la estructura correcta
        if rol == 'paciente':
            # Separar nombre completo en nombre y apellido si viene junto
            partes_nombre = nombre.split(' ', 1)
            nombre_paciente = partes_nombre[0]
            apellido_paciente = apellido if apellido else (partes_nombre[1] if len(partes_nombre) > 1 else '')
            
            # Formato de fecha como string "YYYY-MM-DD HH:MM:SS"
            fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            paciente = {
                'cedula': cedula,
                'nombre': nombre_paciente,
                'apellido': apellido_paciente,
                'fecha_nacimiento': fecha_nacimiento if fecha_nacimiento else '',
                'telefono': telefono,
                'email': email,
                'telegram_user_id': telegram_user_id if telegram_user_id else '',
                'activo': True,
                'fecha_registro': fecha_actual,
                'fecha_actualizacion': fecha_actual
            }
            
            db.pacientes.insert_one(paciente)
        
        return True
    except Exception as e:
        print(f"Error al crear usuario: {e}")
        return False


def autenticar_usuario(cedula, password):
    """Autentica un usuario y devuelve sus datos si es válido"""
    if db is None:
        return None
    
    try:
        usuario = db.usuarios.find_one({'cedula': cedula, 'activo': True})
        
        if usuario and check_password_hash(usuario['password'], password):
            # Eliminar el password del objeto retornado
            usuario_sin_password = {
                'cedula': usuario['cedula'],
                'nombre': usuario['nombre'],
                'email': usuario['email'],
                'telefono': usuario['telefono'],
                'rol': usuario['rol'],
                'especialidad': usuario.get('especialidad', '')
            }
            return usuario_sin_password
        
        return None
    except Exception as e:
        print(f"Error al autenticar usuario: {e}")
        return None


def obtener_usuario(cedula):
    """Obtiene un usuario por cédula (sin password)"""
    if db is None:
        return None
    
    try:
        usuario = db.usuarios.find_one({'cedula': cedula}, {'password': 0})
        return usuario
    except Exception as e:
        print(f"Error al obtener usuario: {e}")
        return None


def obtener_pacientes():
    """Obtiene la lista de todos los pacientes"""
    if db is None:
        return []
    
    try:
        pacientes = list(db.pacientes.find({}, {'_id': 0, 'cedula': 1, 'nombre': 1}))
        return pacientes
    except Exception as e:
        print(f"Error al obtener pacientes: {e}")
        return []


def usuario_existe(cedula):
    """Verifica si un usuario ya existe"""
    if db is None:
        return False
    
    try:
        return db.usuarios.find_one({'cedula': cedula}) is not None
    except Exception as e:
        print(f"Error al verificar usuario: {e}")
        return False


def actualizar_usuario(cedula, datos):
    """Actualiza los datos de un usuario"""
    if db is None:
        return False
    
    try:
        db.usuarios.update_one(
            {'cedula': cedula},
            {'$set': datos}
        )
        return True
    except Exception as e:
        print(f"Error al actualizar usuario: {e}")
        return False


def inicializar_datos_prueba():
    """Inicializa la base de datos con usuarios de prueba si está vacía"""
    if db is None:
        print("⚠️ No se puede inicializar: db es None")
        return
    
    try:
        # Verificar si ya existen usuarios
        if db.usuarios.count_documents({}) > 0:
            print("ℹ️ La base de datos ya tiene usuarios")
            return
        
        print("📝 Inicializando usuarios de prueba...")
        
        # Crear pacientes de prueba
        crear_usuario(
            cedula='123456789',
            nombre='Juan Pérez',
            email='juan@example.com',
            telefono='3001234567',
            password='paciente123',
            rol='paciente'
        )
        
        crear_usuario(
            cedula='987654321',
            nombre='Ana Martínez',
            email='ana@example.com',
            telefono='3002345678',
            password='paciente456',
            rol='paciente'
        )
        
        crear_usuario(
            cedula='555666777',
            nombre='Carlos López',
            email='carlos@example.com',
            telefono='3003456789',
            password='paciente789',
            rol='paciente'
        )
        
        # Crear médico de prueba
        crear_usuario(
            cedula='doc001',
            nombre='Dra. María González',
            email='maria@hospital.com',
            telefono='3009876543',
            password='medico123',
            rol='medico',
            especialidad='Cardiología'
        )
        
        print("✅ Usuarios de prueba creados exitosamente")
        
    except Exception as e:
        print(f"❌ Error al inicializar datos de prueba: {e}")


def cerrar_conexion():
    """Cierra la conexión con MongoDB"""
    if client:
        client.close()
        print("🔌 Conexión con MongoDB cerrada")