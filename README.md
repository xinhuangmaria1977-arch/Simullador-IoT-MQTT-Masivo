# Simulador de Redes IoT Masivas (MQTT Benchmarking & Monitoring)

Este proyecto implementa un entorno de pruebas de estres y monitorizacion en tiempo real para brokers MQTT. Permite simular el comportamiento concurrente de 1.000 dispositivos IoT virtuales transmitiendo telemetria continua mediante programacion asincrona, capturando y clasificando los eventos criticos desde una consola centralizada.

## Arquitectura y Tecnologias
* **Infraestructura:** Despliegue del broker Eclipse Mosquitto encapsulado mediante **Docker**.
* **Protocolo de Red:** MQTT sobre TCP/IP con control de flujo de calidad de servicio (QoS 1).
* **Concurrencia:** Simulación masiva asincrona mediante **Python (Asyncio)** evitando bloqueos de sockets (Thundering Herd).
* **Procesamiento en Tiempo Real:** Consola centralizada con filtros dinamicos mediante comodines MQTT (+) y metricas en vivo.

## Requisitos
* Docker / Docker Desktop
* Python 3.8 o superior
* Libreria paho-mqtt (pip install paho-mqtt)

## Instrucciones de Uso

### 1. Levantar el Servidor (Broker)
Inicia el contenedor de Docker desde tu terminal:
`bash
docker start mi_broker_mqtt
`",
",

Arranca la consola central de control de eventos, alarmas y contadores:
`bash
python Simulador/receptor.py
`",
",

Arranca el motor asincrono para desplegar los 1.000 sensores virtuales de forma progresiva:
`bash
python Simulador/simulador_masivo.py
`",
",

* **Ramping de conexiones:** Algoritmo de escalado progresivo (pausas de 500ms cada 50 conexiones) para proteger los sockets del sistema operativo.
* **Filtros Inteligentes:** Uso del comodin 	eleco/+/temperatura para delegar el filtrado de red de los 1.000 canales en el Broker.
* **Procesamiento de Eventos:** Clasificacion en vivo de lecturas normales ([OK]) y condiciones de sobrecalentamiento ([ALERTA CRITICA] > 32C).
* **UI Optimizada:** Panel dinamico en consola mediante retornos de carro interactivos (end='\r') que evitan la saturacion de la terminal.
