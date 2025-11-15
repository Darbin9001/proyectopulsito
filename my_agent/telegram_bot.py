import os
import sys
from pathlib import Path
import re
import requests

sys.path.append(str(Path(__file__).resolve().parent.parent))

from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes, ConversationHandler
from my_agent.agent import root_agent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
SERVICE2_URL = "http://127.0.0.1:8002"  # Service2 en puerto 8002

# Estados de conversación
ESPERANDO_CEDULA, CONVERSACION_NORMAL = range(2)

# Crear el runner una sola vez al inicio
session_service = InMemorySessionService()
runner = Runner(
    agent=root_agent, 
    session_service=session_service,
    app_name='telegram_bot'
)

# Diccionario para mantener sesiones por usuario de Telegram
user_sessions = {}
user_cedulas = {}  # Para recordar la última cédula consultada por usuario


def extraer_cedula(texto: str) -> str:
    """Extrae una cédula del texto (números de 6-10 dígitos)"""
    match = re.search(r'\b\d{6,10}\b', texto)
    return match.group(0) if match else None


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /start"""
    keyboard = [
        [KeyboardButton("📊 Ver mis signos vitales")],
        [KeyboardButton("📋 Ver historial")],
        [KeyboardButton("👥 Cambiar paciente")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        "👋 ¡Hola! Soy Pulsito, tu asistente médico virtual.\n\n"
        "Para comenzar, por favor indícame el número de cédula del paciente:",
        reply_markup=reply_markup
    )
    return ESPERANDO_CEDULA


async def recibir_cedula(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Recibe y valida la cédula del paciente"""
    user_id = str(update.effective_user.id)
    texto = update.message.text
    
    # Si el usuario presiona un botón antes de dar la cédula
    if texto in ["📊 Ver mis signos vitales", "📋 Ver historial", "👥 Cambiar paciente"]:
        await update.message.reply_text(
            "Primero necesito que me proporciones el número de cédula del paciente."
        )
        return ESPERANDO_CEDULA
    
    cedula = extraer_cedula(texto)
    
    if not cedula:
        await update.message.reply_text(
            "❌ No pude identificar una cédula válida.\n"
            "Por favor, envía solo el número de cédula (6-10 dígitos)."
        )
        return ESPERANDO_CEDULA
    
    # Verificar si el paciente existe consultando service2
    try:
        response = requests.get(f"{SERVICE2_URL}/analyze/{cedula}", timeout=5)
        
        if response.status_code == 404:
            await update.message.reply_text(
                f"❌ No encontré registros para la cédula {cedula}.\n\n"
                "Asegúrate de que el paciente esté registrado y tenga signos vitales."
            )
            return ESPERANDO_CEDULA
        
        if response.status_code != 200:
            await update.message.reply_text(
                "⚠️ Hubo un problema al consultar los datos. Intenta de nuevo."
            )
            return ESPERANDO_CEDULA
        
        data = response.json()
        paciente_nombre = data.get("paciente", {}).get("nombre", "Desconocido")
        
        # Guardar la cédula para este usuario
        user_cedulas[user_id] = cedula
        
        await update.message.reply_text(
            f"✅ Paciente encontrado: {paciente_nombre}\n"
            f"Cédula: {cedula}\n\n"
            "Ahora puedes preguntarme sobre sus signos vitales."
        )
        
        return CONVERSACION_NORMAL
        
    except requests.exceptions.Timeout:
        await update.message.reply_text(
            "⏱️ La consulta está tardando mucho. Verifica que los servicios estén activos."
        )
        return ESPERANDO_CEDULA
    except Exception as e:
        print(f"❌ Error: {e}")
        await update.message.reply_text(
            "❌ Ocurrió un error al verificar la cédula. Intenta nuevamente."
        )
        return ESPERANDO_CEDULA


async def cambiar_paciente(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Permite cambiar de paciente"""
    await update.message.reply_text(
        "Por favor, indícame el nuevo número de cédula del paciente:"
    )
    return ESPERANDO_CEDULA


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Maneja los mensajes del usuario cuando ya tiene una cédula asignada"""
    user_message = update.message.text
    user_id = str(update.effective_user.id)
    
    # Verificar si es un botón
    if user_message == "📊 Ver mis signos vitales":
        user_message = "¿Cuáles son los últimos signos vitales?"
    elif user_message == "📋 Ver historial":
        user_message = "Muéstrame el historial de signos vitales"
    elif user_message == "👥 Cambiar paciente":
        return await cambiar_paciente(update, context)
    
    cedula = user_cedulas.get(user_id)
    
    if not cedula:
        await update.message.reply_text(
            "⚠️ Primero necesito saber la cédula del paciente.\n"
            "Usa el botón '👥 Cambiar paciente' o envía la cédula."
        )
        return ESPERANDO_CEDULA
    
    print(f"📩 Mensaje de {user_id} para cédula {cedula}: {user_message}")

    try:
        # Obtener los datos más recientes desde Service2
        response = requests.get(f"{SERVICE2_URL}/analyze/{cedula}", timeout=10)
        
        if response.status_code == 404:
            await update.message.reply_text(
                f"⚠️ No hay datos disponibles para la cédula {cedula}.\n"
                "Puede que el paciente no tenga registros recientes."
            )
            return CONVERSACION_NORMAL
        
        if response.status_code != 200:
            contexto = "⚠️ No se pudieron obtener los signos vitales recientes.\n\n"
        else:
            health_data = response.json()
            
            if "datos" in health_data:
                datos = health_data["datos"]
                paciente = health_data.get("paciente", {})
                alertas = health_data.get("alertas", [])
                
                contexto = (
                    f"📊 **Paciente:** {paciente.get('nombre', 'Desconocido')}\n"
                    f"📋 **Cédula:** {cedula}\n"
                    f"🕐 **Última lectura:** {health_data.get('timestamp', 'N/A')}\n\n"
                    f"**Signos vitales:**\n"
                    f"❤️ Ritmo cardíaco: {datos.get('ritmo_cardiaco', 'N/A')} bpm\n"
                    f"🌡️ Temperatura: {datos.get('temperatura', 'N/A')} °C\n"
                    f"💉 Presión arterial: {datos.get('presion', 'N/A')}\n"
                    f"🫁 Saturación de oxígeno: {datos.get('oxigeno', 'N/A')} %\n\n"
                    f"**Alertas:** {', '.join(alertas)}\n\n"
                )
            else:
                contexto = "⚠️ No se encontraron datos estructurados.\n\n"

        # Crear el contenido del mensaje del usuario con contexto clínico
        message_text = contexto + f"Consulta del usuario: {user_message}"

        # Obtener o crear sesión para este usuario
        if user_id not in user_sessions:
            session = await session_service.create_session(
                app_name='telegram_bot',
                user_id=user_id,
                session_id=f'session_{user_id}'
            )
            user_sessions[user_id] = session.id
        
        session_id = user_sessions[user_id]

        # Crear el contenido del mensaje
        message = types.Content(
            role='user',
            parts=[types.Part(text=message_text)]
        )
        
        # Ejecutar el agente con el runner
        response_text = ""
        async for event in runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=message
        ):
            if event.is_final_response():
                if event.content and event.content.parts:
                    for part in event.content.parts:
                        if hasattr(part, 'text') and part.text:
                            response_text += part.text
        
        if not response_text:
            response_text = "No pude generar una respuesta."

        print(f"🤖 Respuesta: {response_text[:150]}...")
        await update.message.reply_text(response_text)
        
        return CONVERSACION_NORMAL
        
    except requests.exceptions.Timeout:
        await update.message.reply_text(
            "⏱️ La consulta está tardando mucho. Los servicios pueden estar lentos."
        )
        return CONVERSACION_NORMAL
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        await update.message.reply_text(
            "❌ Ocurrió un error al procesar tu mensaje. Intenta nuevamente."
        )
        return CONVERSACION_NORMAL


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancela la conversación"""
    await update.message.reply_text(
        "Conversación cancelada. Usa /start para comenzar de nuevo."
    )
    return ConversationHandler.END


if __name__ == "__main__":
    if not TOKEN:
        print("❌ Falta el token de Telegram en la variable TELEGRAM_TOKEN")
        exit(1)

    app = ApplicationBuilder().token(TOKEN).build()

    # Manejador de conversación
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ESPERANDO_CEDULA: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_cedula)
            ],
            CONVERSACION_NORMAL: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)

    print("✅ Bot de Telegram conectado y esperando mensajes...")
    app.run_polling()