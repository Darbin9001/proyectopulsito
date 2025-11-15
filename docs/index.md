# 🩺 Sistema de Monitoreo de Salud

## 📘 Descripción General

El **Sistema de Monitoreo de Salud** es una aplicación desarrollada en Python basada en microservicios, diseñada para el **seguimiento continuo y remoto de signos vitales** de pacientes.  
Este sistema permite **registrar, visualizar y analizar datos biomédicos** de manera automatizada, generando alertas ante valores críticos y ofreciendo una herramienta de apoyo para la toma de decisiones clínicas.

El proyecto aplica **buenas prácticas de desarrollo de software**, incluyendo:
- Entornos virtuales (`venv`)
- Control de versiones (`Git / GitHub`)
- Contenedorización con `Docker`
- Pruebas automatizadas con `Pytest`
- Documentación técnica con `MkDocs`

---

## 🎯 Objetivo General

Desarrollar un sistema de monitoreo de salud que permita registrar, visualizar y alertar en tiempo real sobre variaciones críticas en los signos vitales de pacientes, utilizando buenas prácticas de desarrollo de software en Python, con el fin de mejorar la atención remota y la toma de decisiones clínicas oportunas.

---

## 🎯 Objetivos Específicos

1. Identificar y documentar los requerimientos funcionales y no funcionales del sistema.  
2. Diseñar la arquitectura del sistema utilizando principios de diseño modular y diagramas UML.  
3. Desarrollar los microservicios en Python integrando `Flask` y `FastAPI`.  
4. Implementar pruebas automatizadas con `Pytest` y documentación con `MkDocs`.  
5. Contenerizar los servicios utilizando `Docker` y orquestarlos con `docker-compose`.

---

## 🏗️ Arquitectura del Sistema

El sistema está compuesto por varios módulos:

- **API Gateway**: canal de comunicación entre el frontend y los microservicios.
- **Frontend**: interfaz web para la visualización de los signos vitales y alertas.
- **Microservicios**:
  - `authentication`: manejo de usuarios y control de acceso.
  - `vitales`: gestión de datos biomédicos (frecuencia cardíaca, presión arterial, temperatura, etc.).
  - `analisis`: procesamiento y generación de alertas ante valores anormales.
  - `notificaciones`: envío de correos o mensajes de alerta a los médicos o cuidadores.

---

## ⚙️ Tecnologías Utilizadas

| Categoría | Herramienta / Tecnología |
|------------|--------------------------|
| Lenguaje | Python 3 |
| Framework web | Flask / FastAPI |
| Base de datos | MongoDB |
| Virtualización | Docker / Docker Compose |
| Pruebas | Pytest |
| Documentación | MkDocs (Material Theme + PlantUML) |
| Control de versiones | Git / GitHub |

---

## 🧩 Estructura del Proyecto

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
