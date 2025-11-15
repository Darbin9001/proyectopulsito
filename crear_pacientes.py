"""
Script para registrar pacientes de prueba en el sistema
Ejecutar: python registrar_pacientes.py
"""

import requests
import time

SERVICE1_URL = "http://127.0.0.1:8001"

# Pacientes de prueba
pacientes = [
    {
        "cedula": "1234567890",
        "nombre": "Juan",
        "apellido": "Pérez",
        "edad": 45
    },
    {
        "cedula": "9876543210",
        "nombre": "María",
        "apellido": "González",
        "edad": 32
    },
    {
        "cedula": "654321987",
        "nombre": "Carlos",
        "apellido": "Rodríguez",
        "edad": 58
    }
]

def registrar_pacientes():
    print("🏥 Registrando pacientes de prueba...\n")
    
    for paciente in pacientes:
        try:
            # Registrar paciente
            response = requests.post(
                f"{SERVICE1_URL}/pacientes",
                params=paciente,
                timeout=5
            )
            
            if response.status_code == 200:
                print(f"✅ {paciente['nombre']} {paciente['apellido']} - Cédula: {paciente['cedula']}")
            else:
                print(f"❌ Error registrando {paciente['nombre']}: {response.text}")
            
            time.sleep(1)
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n✅ Registro completado!")


def generar_signos_vitales():
    print("\n📊 Generando signos vitales iniciales para cada paciente...\n")
    
    for paciente in pacientes:
        cedula = paciente["cedula"]
        try:
            # Generar 3 lecturas para cada paciente
            for i in range(3):
                response = requests.post(
                    f"{SERVICE1_URL}/health-data/{cedula}",
                    timeout=5
                )
                
                if response.status_code == 200:
                    data = response.json()
                    lectura = data.get("lectura", {})
                    print(f"  ✅ Lectura {i+1} para {paciente['nombre']}: "
                          f"BPM={lectura.get('ritmo_cardiaco')}, "
                          f"Temp={lectura.get('temperatura')}°C")
                else:
                    print(f"  ❌ Error generando datos para {paciente['nombre']}")
                
                time.sleep(2)  # Esperar 2 segundos entre lecturas
            
            print()
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("✅ Signos vitales generados!")


if __name__ == "__main__":
    print("=" * 60)
    print("  CONFIGURACIÓN INICIAL DEL SISTEMA DE MONITOREO")
    print("=" * 60)
    print()
    
    # Verificar que el servicio esté activo
    try:
        response = requests.get(f"{SERVICE1_URL}/", timeout=5)
        if response.status_code == 200:
            print("✅ Service1 está activo\n")
        else:
            print("⚠️ Service1 respondió con un código inusual\n")
    except Exception as e:
        print(f"❌ Error: No se puede conectar con Service1 en {SERVICE1_URL}")
        print("   Asegúrate de que el servicio esté corriendo.\n")
        exit(1)
    
    # Paso 1: Registrar pacientes
    registrar_pacientes()
    
    # Paso 2: Generar signos vitales
    generar_signos_vitales()
    
    print("\n" + "=" * 60)
    print("  CONFIGURACIÓN COMPLETADA")
    print("=" * 60)
    print("\n📱 Ahora puedes usar el bot de Telegram con estas cédulas:")
    for p in pacientes:
        print(f"   • {p['cedula']} - {p['nombre']} {p['apellido']}")
    print()