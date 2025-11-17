# 🏥 Sistema de Monitoreo de Salud – Pulsito

### Sistema integral de monitoreo médico con microservicios, IA y bot conversacional

---

## 👥 Equipo de Desarrollo

| Cédula | Nombre | Correo |
|:-------|:-------|:-------|
| 1060872570 | Darbin Garcia Acosta | garcia_9001@hotmail.com |
| 1087189221 | Alex Duvan Perlaza | alexper1806@gmail.com |

---

## 📌 Descripción del Proyecto

**Pulsito** es un sistema completo de monitoreo médico en tiempo real construido con arquitectura de **microservicios**, contenerizado con **Docker**, e integrado con **inteligencia artificial** mediante Google Gemini 2.5 Flash y un **bot de Telegram** para interacción con pacientes.

### ✨ Características Principales

- 📊 **Generación automática** de signos vitales en tiempo real
- 🧠 **Análisis inteligente** con reglas médicas y alertas
- 🤖 **Agente de IA médica** con Gemini 2.5 Flash
- 💬 **Bot conversacional** de Telegram para pacientes
- 🖥️ **Dashboard web** con visualización de datos
- 🧱 **Orquestación completa** con Docker Compose
- 🔒 **Sistema de autenticación** con roles (médico/paciente)

---

## 🎯 Objetivos del Proyecto

- ✅ Diseñar microservicios independientes y escalables
- ✅ Implementar APIs REST con FastAPI y Flask
- ✅ Utilizar MongoDB Atlas como base de datos en la nube
- ✅ Crear un frontend dinámico con visualización en tiempo real
- ✅ Integrar un agente conversacional basado en IA
- ✅ Contenerizar toda la aplicación con Docker
- ✅ Automatizar la generación de datos médicos de prueba

---

## 🏗 Arquitectura del Sistema

```mermaid
graph TB
    subgraph "Capa de Usuarios"
        A[Frontend Web]
        B[Bot Telegram]
        C[Generador Automático]
    end
    
    subgraph "API Gateway"
        D[API Gateway :8000]
    end
    
    subgraph "Microservicios"
        E[Auth Service :8001]
        F[Service1 Pacientes :8002]
        G[Service2 Análisis :8003]
    end
    
    subgraph "Base de Datos"
        H[MongoDB Atlas]
        I[data_history.json]
    end
    
    A --> D
    B --> D
    C --> F
    D --> E
    D --> F
    D --> G
    F --> H
    E --> H
    G --> F
    G --> I
```

---

## 📂 Estructura del Proyecto

```
proyecto-pulsito/
│
├── 📁 frontend/                 # Dashboard web (Flask)
│   ├── templates/               # Plantillas HTML
│   ├── static/                  # CSS, JS, recursos
│   ├── app.py                   # Aplicación principal
│   └── Dockerfile
│
├── 📁 api-gateway/              # Punto de entrada unificado
│   ├── main.py                  # Router principal
│   └── Dockerfile
│
├── 📁 services/
│   ├── authentication/          # Servicio de login y usuarios
│   │   ├── main.py
│   │   └── Dockerfile
│   │
│   ├── service1/                # Gestión de pacientes y signos vitales
│   │   ├── main.py
│   │   ├── models.py
│   │   └── Dockerfile
│   │
│   ├── service2/                # Análisis médico y alertas
│   │   ├── main.py
│   │   ├── models.py
│   │   └── Dockerfile
│   │
│   ├── data_base_mongo.py       # Módulo compartido de MongoDB
│   └── utils.py                 # Utilidades compartidas
│
├── 📁 my_agent/                 # Bot de Telegram + IA
│   ├── telegram_bot.py          # Bot conversacional
│   ├── agent.py                 # Agente de IA con Gemini
│   └── Dockerfile
│
├── 📁 docs/                     # Documentación del proyecto
│   └── uml/                     # Diagramas UML
│
├── 📄 docker-compose.yml        # Orquestación de servicios
├── 📄 .env                      # Variables de entorno
├── 📄 data_history.json         # Historial persistente
└── 📄 README.md                 # Este archivo
```

---

## 🧪 Microservicios

### 🔐 **Auth Service** (Puerto 8001)

**Responsabilidades:**
- Autenticación de usuarios (médicos y pacientes)
- Gestión de sesiones
- Validación de credenciales

**Endpoints principales:**
```
POST /login
POST /register
GET  /usuarios/{cedula}
```

---

### 👥 **Service1 - Pacientes** (Puerto 8002)

**Responsabilidades:**
- Registro y gestión de pacientes
- Almacenamiento de signos vitales
- Consulta de datos históricos

**Endpoints principales:**
```
GET  /pacientes
GET  /pacientes/{cedula}
POST /pacientes
POST /health-data/{cedula}
GET  /health-data/{cedula}
```

---

### 📊 **Service2 - Análisis** (Puerto 8003)

**Responsabilidades:**
- Análisis de signos vitales
- Generación de alertas médicas:
  - 🌡️ **Fiebre** (temperatura > 38°C)
  - ❤️ **Taquicardia** (ritmo cardíaco > 100 bpm)
  - 🫁 **Hipoxia** (saturación O₂ < 95%)
- Almacenamiento de historial clínico

**Endpoints principales:**
```
GET  /analyze/{cedula}
GET  /historial/{cedula}
GET  /pacientes
```

---

### 🚪 **API Gateway** (Puerto 8000)

**Responsabilidades:**
- Punto de entrada único al sistema
- Enrutamiento a microservicios
- Centralización de logs

---

### 💬 **Bot de Telegram**

**Funcionalidades:**
- Consulta de signos vitales por cédula
- Visualización de alertas médicas
- Explicaciones en lenguaje natural con IA
- Recomendaciones personalizadas

**Comandos:**
```
/start - Iniciar conversación
📊 Ver mis signos vitales
📋 Ver historial
👥 Cambiar paciente
```

---

## 🤖 Inteligencia Artificial

El sistema integra **Google Gemini 2.5 Flash** mediante el SDK de Google ADK:

- 🧠 **Razonamiento médico** sobre datos del paciente
- 💡 **Explicaciones** en lenguaje natural
- 📋 **Recomendaciones** personalizadas
- ⚠️ **Detección de riesgos** y alertas tempranas

### Ejemplo de interacción:

```
Usuario: ¿Cuál es mi estado de salud actual?

Pulsito: Según tu última lectura:
- Tu ritmo cardíaco es 102 bpm (ligeramente elevado)
- Temperatura normal: 36.8°C
- Saturación de oxígeno: 98% (excelente)

⚠️ Recomendación: Tu ritmo cardíaco está un poco alto.
Intenta relajarte y evita el estrés. Si persiste, consulta a tu médico.
```

---

## 🐳 Instalación y Ejecución

### Prerrequisitos

- Docker y Docker Compose instalados
- Cuenta de MongoDB Atlas (o MongoDB local)
- Token de Bot de Telegram (opcional)
- Google API Key (opcional, para IA)

### 1️⃣ Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/proyecto-pulsito.git
cd proyecto-pulsito
```

### 2️⃣ Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
# MongoDB (OBLIGATORIO)
MONGO_URI=mongodb+srv://usuario:password@cluster.mongodb.net/?retryWrites=true&w=majority
DB_NAME=pulsito_db

# Telegram Bot (OPCIONAL)
TELEGRAM_TOKEN=tu_token_de_telegram

# Google AI (OPCIONAL)
GOOGLE_API_KEY=tu_api_key_de_google

# Flask
SECRET_KEY=clave_secreta_super_segura
```
> ⚠️ **IMPORTANTE - Configuración de MongoDB Atlas:**
> 
> Si vas a desplegar este sistema en otro computador o servidor, **debes agregar la IP pública de esa máquina en la lista de IPs permitidas de MongoDB Atlas**, de lo contrario los servicios no podrán conectarse a la base de datos.
>
> **Pasos para configurar el acceso:**
> 1. Accede a [MongoDB Atlas](https://cloud.mongodb.com/)
> 2. Ve a tu cluster → **Network Access**
> 3. Click en **Add IP Address**
> 4. Agrega la IP pública del servidor/computador
> 5. O selecciona **Allow Access from Anywhere** (0.0.0.0/0) para desarrollo
>
> 💡 **Tip:** Para encontrar tu IP pública, visita: https://www.whatismyip.com/

### 3️⃣ Levantar todos los servicios

```bash
# Construir y levantar todos los contenedores
docker-compose up --build

# O en segundo plano
docker-compose up -d
```

### 4️⃣ Verificar que todo funciona

```bash
# Ver logs de todos los servicios
docker-compose logs -f

# Ver servicios en ejecución
docker-compose ps
```

---

## 🌐 Acceso a los Servicios

| Servicio | URL | Descripción |
|:---------|:----|:------------|
| Frontend | http://localhost:5000 | Dashboard web |
| API Gateway | http://localhost:8000 | Punto de entrada API |
| Auth Service | http://localhost:8001 | Autenticación |
| Service1 | http://localhost:8002 | Gestión pacientes |
| Service2 | http://localhost:8003 | Análisis médico |
| Bot Telegram | Telegram App | Bot conversacional |

---

## 🧪 Datos de Prueba

El sistema incluye usuarios predeterminados:

### Pacientes:
```
Cédula: 123456789
Password: paciente123

Cédula: 987654321
Password: paciente456
```

### Médicos:
```
Cédula: doc001
Password: medico123
Especialidad: Cardiología
```

---

## 📊 Pruebas de API

### Crear un paciente
```bash
curl -X POST http://localhost:8002/pacientes \
  -H "Content-Type: application/json" \
  -d '{
    "cedula": "111222333",
    "nombre": "Juan",
    "apellido": "Pérez",
    "edad": 30
  }'
```

### Generar signos vitales
```bash
curl -X POST http://localhost:8002/health-data/111222333
```

### Analizar signos vitales
```bash
curl http://localhost:8003/analyze/111222333
```

### Ver historial
```bash
curl http://localhost:8003/historial/111222333
```

---

## 🛠 Comandos Útiles de Docker

```bash
# Detener todos los servicios
docker-compose down

# Reconstruir un servicio específico
docker-compose build service1-service

# Ver logs de un servicio
docker-compose logs -f frontend

# Reiniciar un servicio
docker-compose restart service2-service

# Entrar a un contenedor
docker exec -it service1-service bash

# Limpiar todo (contenedores, imágenes, volúmenes)
docker-compose down --rmi all --volumes
```

---

## 🚨 Troubleshooting

### ❌ Bot de Telegram no responde

**Solución:**
- Verifica que `TELEGRAM_TOKEN` esté configurado correctamente
- Revisa los logs: `docker-compose logs -f telegram-agent`

### ❌ Error de conexión a MongoDB

**Solución:**
- Verifica que `MONGO_URI` y `DB_NAME` estén en el `.env`
- Asegúrate de permitir conexiones desde cualquier IP en MongoDB Atlas

### ❌ Service2 no carga datos históricos

**Solución:**
- Verifica que `data_history.json` exista en la raíz
- Asegúrate de que el volumen esté mapeado en `docker-compose.yml`:
```yaml
volumes:
  - ./data_history.json:/app/data_history.json
```

### ❌ Frontend no encuentra módulos

**Solución:**
- Verifica que el Dockerfile copie los módulos compartidos:
```dockerfile
COPY services/data_base_mongo.py services/utils.py ./
```

---

## 📈 Próximas Mejoras

- [ ] Notificaciones push automáticas para alertas críticas
- [ ] Integración con dispositivos IoT (wearables)
- [ ] Generación de reportes médicos en PDF
- [ ] Panel de administración avanzado para médicos
- [ ] Autenticación JWT con tokens de sesión
- [ ] Graficas avanzadas con D3.js o Plotly
- [ ] Exportación de datos a CSV/Excel
- [ ] Sistema de videollamadas médicas

---

## 📚 Tecnologías Utilizadas

| Tecnología | Uso |
|:-----------|:----|
| Python 3.11+ | Backend |
| FastAPI | APIs REST |
| Flask | Frontend |
| MongoDB Atlas | Base de datos |
| Docker & Docker Compose | Contenerización |
| Telegram Bot API | Bot conversacional |
| Google Gemini 2.5 Flash | IA Generativa |

---

## 📄 Licencia

Este proyecto fue desarrollado como parte del **Seminario de Ingeniería** en la **Universidad Remington**.

---

## 👨‍💻 Créditos

Desarrollado con ❤️ por **Darbin Garcia** & **Alex Perlaza**

Universidad Remington - 2025

---

### ⭐ Si te gusta el proyecto, dale una estrella ⭐