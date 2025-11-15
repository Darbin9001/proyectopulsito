# Diagrama de Clases

Representación de las clases principales del sistema y sus relaciones.

```mermaid
classDiagram
  class Usuario {
    +int id
    +string nombre
    +string email
    +string rol
    +bool autenticar()
  }

  class Vital {
    +int id
    +int paciente_id
    +float frecuencia_cardiaca
    +float temperatura
    +string presion
    +void registrar_datos()
    +dict generar_datos_aleatorios()
  }

  class Alerta {
    +int id
    +int paciente_id
    +string tipo
    +string nivel
    +string mensaje
    +bool evaluar_vitales(v: Vital)
  }

  class Notificacion {
    +int id
    +int alerta_id
    +string tipo
    +void enviar()
  }

  class ServicioAnalisis {
    +Alerta procesar_datos(vital: Vital)
    +list reglas_alertas
  }

  Usuario "1" --> "0..*" Vital
  Vital "1" --> "0..*" Alerta
  Alerta "1" --> "1" Notificacion
  ServicioAnalisis "1" --> "0..*" Vital
