# Casos de Uso

Este diagrama muestra los actores y casos de uso principales del sistema.

```mermaid
flowchart LR
  actorPaciente(["👤 Paciente"])
  actorMedico(["🩺 Médico"])

  subgraph Sistema_de_Monitoreo_de_Salud
    UC1["Iniciar Sesión"]
    UC2["Visualizar Signos Vitales"]
    UC3["Recibir Alertas"]
    UC4["Registrar Paciente"]
    UC5["Analizar Métricas"]
  end

  actorPaciente --> UC1
  actorPaciente --> UC2
  actorPaciente --> UC3

  actorMedico --> UC1
  actorMedico --> UC2
  actorMedico --> UC3
  actorMedico --> UC4
  actorMedico --> UC5
