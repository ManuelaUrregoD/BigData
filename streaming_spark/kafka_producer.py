import time
import json
import random
from kafka import KafkaProducer

# Posibles valores simulados
paises = ["Colombia", "México", "Argentina", "Chile", "Perú"]
generos = ["masculino", "femenino"]

def generar_datos_suicidio():
    return {
        "pais": random.choice(paises),
        "anio": random.randint(2010, 2022),
        "genero": random.choice(generos),
        "numero_suicidios": random.randint(1, 50),
        "poblacion": random.randint(100000, 5000000),
        "marca_tiempo": int(time.time())
    }

# Configurar productor Kafka
productor = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

# Envío continuo de mensajes
while True:
    datos = generar_datos_suicidio()
    productor.send('suicidios_data', value=datos)
    print(f"Enviado: {datos}")
    time.sleep(1)
