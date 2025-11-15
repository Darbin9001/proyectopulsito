# Diagrama de Secuencia

Muestra el flujo de interacción entre los actores y componentes del sistema.

```mermaid
sequenceDiagram
  actor Paciente
  participant App as "App Móvil"
  participant API as "API de Salud"
  participant Analisis as "Servicio de Análisis"
  participant DB as "Base de Datos"
  participant Medico as "Médico"

  Paciente->>App: Registrar datos vitales
  App->>API: Enviar datos JSON
  API->>Analisis: Procesar datos()
  Analisis->>DB: Guardar registro
  Analisis->>API: Retornar resultado
  API->>App: Mostrar notificación
  App->>Medico: Enviar alerta
