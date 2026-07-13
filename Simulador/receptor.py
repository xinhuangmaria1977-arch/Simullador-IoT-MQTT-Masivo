import paho.mqtt.client as mqtt
import os

BROKER_HOST = '127.0.0.1'
BROKER_PORT = 1883
TOPIC_FILTRO = 'teleco/+/temperatura'
UMBRAL_MAXIMO = 32.0

contador_ok = 0
contador_critico = 0

def actualizar_pantalla():
    # Este comando limpia la pantalla por completo tanto en Windows (cls) como en Linux/Mac (clear)
    os.system('cls' if os.name == 'nt' else 'clear')
    print('============================================================', flush=True)
    print('        ESTADO DE LA RED DE SENSORES EN TIEMPO REAL        ', flush=True)
    print('============================================================', flush=True)
    print(f' [OK] Lecturas normales:      {contador_ok}', flush=True)
    print(f' [!!!] Alertas criticas:       {contador_critico}', flush=True)
    print('------------------------------------------------------------', flush=True)
    print(' Presiona Ctrl+C para salir y apagar la consola.', flush=True)

def on_connect(client, userdata, flags, rc, properties=None):
    client.subscribe(TOPIC_FILTRO, qos=1)
    actualizar_pantalla()

def on_message(client, userdata, msg):
    global contador_ok, contador_critico
    try:
        temperatura = float(msg.payload.decode('utf-8'))
        
        if temperatura > UMBRAL_MAXIMO:
            contador_critico += 1
        else:
            contador_ok += 1
        
        # Cada vez que llega un mensaje, limpiamos y redibujamos el cuadro fijo
        actualizar_pantalla()
            
    except ValueError:
        pass

def main():
    cliente = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2, client_id='Consola_Contador_Fijo')
    cliente.on_connect = on_connect
    cliente.on_message = on_message

    try:
        cliente.connect(BROKER_HOST, BROKER_PORT, keepalive=60)
        cliente.loop_forever()
    except KeyboardInterrupt:
        print('\\n[-] Panel de contadores cerrado.', flush=True)
    except Exception as e:
        print(f'\\n[X] Error: {e}', flush=True)

if __name__ == '__main__':
    main()
