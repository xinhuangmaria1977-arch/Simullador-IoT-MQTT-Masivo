import asyncio
import random
import paho.mqtt.client as mqtt

BROKER_HOST = '127.0.0.1'
BROKER_PORT = 1883
TOTAL_SENSORES = 1000  # ¡Subimos a las 4 cifras!

async def simular_dispositivo(id_dispositivo):
    client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2, client_id=f'Sensor_{id_dispositivo}')
    
    try:
        # Conectamos de forma asincrona sin bloquear el hilo
        client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)
        client.loop_start()
        
        # Cada 100 sensores imprimiendo un aviso para no saturar la terminal
        if id_dispositivo % 100 == 0:
            print(f'[+] Hito alcanzado: {id_dispositivo} sensores conectados.', flush=True)
        
        # Bucle infinito enviando datos de forma continua
        while True:
            temperatura = round(random.uniform(18.0, 35.0), 2)
            topic = f'teleco/sensor_{id_dispositivo}/temperatura'
            client.publish(topic, payload=str(temperatura), qos=1)
            
            # Espera un tiempo aleatorio entre 5 y 15 segundos para simular telemetria real
            await asyncio.sleep(random.uniform(5.0, 15.0))
            
    except Exception as e:
        print(f'[X] Error critico en Sensor_{id_dispositivo}: {e}', flush=True)

async def main():
    print(f'=== Iniciando Despliegue de {TOTAL_SENSORES} Sensores Simultaneos ===', flush=True)
    
    tareas = []
    for id in range(1, TOTAL_SENSORES + 1):
        tareas.append(asyncio.create_task(simular_dispositivo(id)))
        
        # Control de flujo: metemos una pausa milimetrica cada 50 conexiones
        if id % 50 == 0:
            await asyncio.sleep(0.5)  # Da un respiro al sistema de 500ms
            print(f'[~] Levantando infraestructura... ({id}/{TOTAL_SENSORES})', flush=True)
            
    print('=== Todos los sensores en linea. Emitiendo telemetria... ===', flush=True)
    # Mantenemos las tareas corriendo indefinidamente
    await asyncio.gather(*tareas)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('\n[-] Simulacion detenida por el usuario.', flush=True)
