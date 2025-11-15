# Sistema de Monitoreo de Salud - Pulsito

| Cedula | Nombre | Correo |
|:---|:---|:---|
| 1060872570 | Darbin Garcia Acosta | garcia_9001@hotmail.com |
| 1087189221 | Alex Duvan Perlaza | alexper1806@gmail.com |

---

## Descripción del Proyecto

**Pulsito** es un sistema integral de monitoreo de salud en tiempo real que utiliza microservicios para gestionar signos vitales de pacientes. El sistema incluye:

- 📊 Generación y almacenamiento de signos vitales
- 🔍 Análisis automático con detección de alertas
- 🤖 Agente de IA médico con Gemini 2.5 Flash
- 💬 Interfaz conversacional mediante Telegram
- 🖥️ Dashboard web para visualización en tiempo real

## Objetivos del Proyecto

* ✅ Diseñar microservicios independientes que se comunican entre sí
* ✅ Implementar APIs RESTful con FastAPI y Flask
* ✅ Utilizar MongoDB Atlas como base de datos centralizada
* ✅ Implementar front-end interactivo con Chart.js para monitoreo en tiempo real
* ✅ Integrar agente conversacional de IA con Google ADK
* ✅ Contenerizar aplicaciones con Docker
* ✅ Crear bot de Telegram para acceso móvil

## Arquitectura del Sistema
```
┌─────────────────────────────────────────────────────────────┐
│                       USUARIOS                               │
│  Dashboard Web (Flask) │ Bot Telegram │ Scripts Generadores  │
└─────────────┬──────────┴──────┬───────┴──────────┬──────────┘
              │                 │                   │
              ▼                 ▼                   ▼
┌─────────────────────────────────────────────────────────────┐
│                     MICROSERVICIOS                           │
│  Service1 (Generador)  │  Service2 (Análisis)  │  Agente IA │
│     Puerto: 8001       │     Puerto: 8002      │  (Gemini)  │
└─────────────┬──────────┴──────┬────────────────┴────────────┘
              │                 │
              ▼                 ▼
┌─────────────────────────────────────────────────────────────┐
│                    MongoDB Atlas                             │
│  Colecciones: usuarios, pacientes, signos_vitales          │
└─────────────────────────────────────────────────────────────┘
```

## Estructura del Proyecto
```
proyecto-seminario/
├── frontend/                    # Aplicación web Flask
│   ├── app.py                  # Servidor principal
│   ├── templates/              # Plantillas HTML
│   │   ├── login.html
│   │   ├── registro.html
│   │   ├── paciente_dashboard.html
│   │   └── medico_dashboard.html
│   ├── static/                 # Recursos estáticos
│   │   ├── css/
│   │   └── js/
│   └── Dockerfile
│
├── services/                    # Microservicios
│   ├── data_base_mongo.py      # Módulo compartido MongoDB
│   ├── utils.py                # Utilidades compartidas
│   │
│   ├── service1/               # Generador de signos vitales
│   │   ├── main.py
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   │
│   ├── service2/               # Análisis de datos
│   │   ├── main.py
│   │   ├── data_history.json
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   │
│   └── pacientes/
│       └── generate_auto_data.py  # Script de simulación
│
├── my_agent/                   # Agente conversacional
│   ├── agent.py               # Configuración Gemini
│   ├── telegram_bot.py        # Bot de Telegram
│   ├── health_data.py         # Integración con Service2
│   └── requirements.txt
│
├── .env                       # Variables de entorno
├── docker-compose.yml         # Orquestación (opcional)
└── README.md
```

## Tecnologías Utilizadas

### Backend
- **FastAPI** - Microservicios REST
- **Flask** - Frontend web
- **MongoDB Atlas** - Base de datos NoSQL
- **Python 3.11+** - Lenguaje principal

### Frontend
- **HTML5/CSS3** - Estructura y estilos
- **JavaScript ES6** - Lógica del cliente
- **Chart.js** - Visualización de gráficas

### IA y Chatbot
- **Google ADK** - Framework de agentes
- **Gemini 2.5 Flash** - Modelo de lenguaje
- **python-telegram-bot** - API de Telegram

### DevOps
- **Docker** - Contenedorización
- **Docker Compose** - Orquestación

## Instalación y Configuración

### 1. Clonar el Repositorio
```bash
git clone https://github.com/Darbin9001/plantilla-proyecto.git
cd sistema-monitoreo-salud
```

### 2. Configurar Variables de Entorno

Crea el archivo `.env` en la raíz del proyecto:
```bash
cp .env.example .env
```

Edita `.env` con tus credenciales:
```env
# MongoDB Atlas
MONGO_URI=mongodb+srv://usuario:password@cluster.mongodb.net/dbname?retryWrites=true&w=majority
DB_NAME=health_monitor

# Flask
SECRET_KEY=tu_clave_secreta_muy_segura

# URLs de Servicios
SERVICE2_URL=http://127.0.0.1:8002
NAME1_SERVICE_URL=http://127.0.0.1:8001

# Telegram Bot
TELEGRAM_TOKEN=tu_token_de_botfather

# Google Gemini
GOOGLE_API_KEY=tu_api_key_de_gemini
```

### 3. Instalar Dependencias

#### Opción A: Instalación Local
```bash
# Frontend
cd frontend
pip install -r requirements.txt

# Service 1
cd ../services/service1
pip install -r requirements.txt

# Service 2
cd ../service2
pip install -r requirements.txt

# Agente IA
cd ../../my_agent
pip install -r requirements.txt
```

#### Opción B: Docker (Recomendado)
```bash
docker-compose up --build
```

## Ejecución del Sistema

### Método 1: Ejecución Manual (Desarrollo)

Abre **4 terminales** diferentes:

**Terminal 1 - Service1 (Puerto 8001):**
```bash
cd services/service1
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

**Terminal 2 - Service2 (Puerto 8002):**
```bash
cd services/service2
uvicorn main:app --host 0.0.0.0 --port 8002 --reload
```

**Terminal 3 - Frontend (Puerto 8080):**
```bash
cd frontend
python app.py
```

**Terminal 4 - Bot de Telegram:**
```bash
cd my_agent
python telegram_bot.py
```

### Método 2: Docker Compose (Producción)
```bash
docker-compose up --build
```

Esto levanta automáticamente:
- ✅ Service1 en `http://localhost:8001`
- ✅ Service2 en `http://localhost:8002`
- ✅ Frontend en `http://localhost:8080`

## URLs de Acceso

| Componente | URL | Puerto |
|------------|-----|--------|
| 🖥️ Dashboard Web | http://localhost:8080 | 8080 |
| 🔧 Service1 (API Docs) | http://localhost:8001/docs | 8001 |
| 📊 Service2 (API Docs) | http://localhost:8002/docs | 8002 |
| 💬 Bot Telegram | @TuBotPulsito | - |

## Uso del Sistema

### 1. Dashboard Web

1. Accede a `http://localhost:8080`
2. **Registro**: Crea una cuenta como paciente
3. **Login**: Inicia sesión con tu cédula y contraseña
4. **Dashboard Paciente**: Visualiza tus signos vitales en tiempo real
5. **Dashboard Médico**: (rol médico) Consulta múltiples pacientes

**Usuarios de Prueba:**
- **Paciente**: Cédula `123456789` / Password: `paciente123`
- **Médico**: Cédula `doc001` / Password: `medico123`

### 2. Bot de Telegram

1. Busca tu bot: `@TuBotPulsito`
2. Envía `/start`
3. Proporciona tu número de cédula
4. Pregunta sobre tus signos vitales

**Ejemplos de consultas:**
- "¿Cuáles son mis últimos signos vitales?"
- "¿Está bien mi presión arterial?"
- "Muéstrame mi historial"

### 3. Generación Automática de Datos

Para simular múltiples pacientes:
```bash
cd services/pacientes
python generate_auto_data.py
```

Este script genera signos vitales cada 10 segundos para cédulas de prueba.

## Endpoints Principales

### Service1 - Generador de Signos Vitales
```
POST   /pacientes                    # Crear paciente
GET    /pacientes/{cedula}           # Obtener paciente
POST   /health-data/{cedula}         # Generar signos vitales
GET    /health-data/{cedula}         # Obtener signos vitales
GET    /pacientes                    # Listar todos los pacientes
```

### Service2 - Análisis de Datos
```
GET    /analyze/{cedula}             # Analizar último registro
GET    /historial/{cedula}           # Obtener historial completo
GET    /pacientes                    # Resumen de pacientes con datos
```

## Funcionalidades Destacadas

### 🎯 Detección Automática de Alertas

El sistema analiza automáticamente:
- ⚠️ Taquicardia (BPM > 100)
- ⚠️ Bradicardia (BPM < 60)
- 🌡️ Fiebre (Temp > 38°C)
- ❄️ Hipotermia (Temp < 36°C)
- 🫁 Hipoxia (O₂ < 95%)

### 📊 Visualización en Tiempo Real

- Gráficas interactivas con Chart.js
- Actualización automática cada 5 segundos
- Alertas visuales y sonoras
- Historial de últimos 20 registros

### 🤖 Agente de IA Médico

- Análisis conversacional de signos vitales
- Explicaciones en lenguaje natural
- Recomendaciones personalizadas
- Contexto médico profesional

## Estructura de Base de Datos

### Colección: `usuarios`
```json
{
  "cedula": "123456789",
  "nombre": "Juan Pérez",
  "email": "juan@example.com",
  "password": "hash_bcrypt",
  "rol": "paciente",
  "activo": true
}
```

### Colección: `pacientes`
```json
{
  "cedula": "123456789",
  "nombre": "Juan",
  "apellido": "Pérez",
  "fecha_nacimiento": "1990-01-15",
  "telefono": "3001234567",
  "email": "juan@example.com"
}
```

### Colección: `signos_vitales`
```json
{
  "cedula": "123456789",
  "nombre": "Juan Pérez",
  "ritmo_cardiaco": 75,
  "temperatura": 36.8,
  "presion": "120/80",
  "oxigeno": 98,
  "timestamp": "2025-11-15 14:30:00"
}
```

## Troubleshooting

### Problema: No se conecta a MongoDB
```bash
# Verifica tu MONGO_URI en .env
# Asegúrate de permitir acceso desde tu IP en MongoDB Atlas
```

### Problema: Puerto ocupado
```bash
# Cambia el puerto en app.py o docker-compose.yml
# O detén el proceso que usa el puerto:
lsof -ti:8080 | xargs kill -9
```

### Problema: Bot de Telegram no responde
```bash
# Verifica el token en .env
# Asegúrate de que Service2 esté corriendo
# Revisa los logs: python telegram_bot.py
```

## Próximas Mejoras

- [ ] Notificaciones push para alertas críticas
- [ ] Exportación de reportes en PDF
- [ ] Integración con dispositivos IoT reales
- [ ] Panel de administración avanzado
- [ ] API Gateway para balanceo de carga
- [ ] Autenticación JWT
- [ ] Tests unitarios y de integración

## Contribuciones

Este proyecto fue desarrollado como parte del Seminario de Ingeniería en la Universidad Remington.

## Licencia

Este proyecto es de uso académico y educativo.

---

**Desarrollado con ❤️ para el Seminario de Ingeniería**