import time
import sys
import paho.mqtt.client as mqtt

print("1. Script iniciado. Configurando variables...", flush=True)
BROKER_HOST = "127.0.0.1"  # Forzamos IP local directa en vez de 'localhost'
BROKER_PORT = 1883
TOPIC = "teleco/prueba"

def on_connect(client, userdata, flags, rc, properties=None):
    print(f"-> Callback on_connect ejecutado. Código: {rc}", flush=True)

def on_publish(client, userdata, mid, properties=None):
    print(f"-> Callback on_publish ejecutado. Mensaje ID: {mid}", flush=True)

print("2. Instanciando el cliente MQTT...", flush=True)
cliente = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2, client_id="Dispositivo_Prueba")
cliente.on_connect = on_connect
cliente.on_publish = on_publish

try:
    # Le añadimos un timeout estricto de 5 segundos para que no se quede congelado eternamente
    print(f"3. Intentando conectar a {BROKER_HOST}:{BROKER_PORT} (Timeout: 5s)...", flush=True)
    cliente.connect(BROKER_HOST, BROKER_PORT, keepalive=60, connect_timeout=5)
    print("4. Conexión de socket abierta. Iniciando bucle de red...", flush=True)
    
    cliente.loop_start()
    time.sleep(1)

    mensaje = "Test de Teleco"
    print(f"5. Publicando mensaje...", flush=True)
    cliente.publish(TOPIC, payload=mensaje, qos=1)

    time.sleep(2)
    cliente.loop_stop()
    cliente.disconnect()
    print("6. Proceso terminado con éxito.", flush=True)

except Exception as e:
    print(f"\n❌ Ocurrió un error durante la ejecución: {e}", flush=True)