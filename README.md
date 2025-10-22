# 🧠 Análisis de Suicidios en Antioquia (2007–2021) con PySpark

## 📘 Descripción del proyecto

Este proyecto implementa un **proceso de análisis batch** utilizando **Apache Spark (PySpark)** sobre el conjunto de datos público de **suicidios reportados en el departamento de Antioquia entre los años 2007 y 2021**, disponible en el portal de [Datos Abiertos de Colombia](https://www.datos.gov.co/).

El objetivo es aplicar las capacidades de **procesamiento distribuido de Spark** para limpiar, transformar y analizar un volumen considerable de información sobre mortalidad por suicidio, generando estadísticas útiles y almacenando los resultados procesados para análisis posteriores.

---

## 🎯 Objetivos

- Cargar y procesar un conjunto de datos de gran tamaño desde una fuente pública.  
- Realizar **limpieza y transformación** de datos usando **RDDs o DataFrames**.  
- Ejecutar un **análisis exploratorio (EDA)** para identificar patrones en el tiempo y en los municipios.  
- Almacenar los resultados procesados en formatos **CSV** y **Parquet** para su posterior consumo o visualización.  

---

## 🧩 Dataset

- **Nombre:** Cantidad de suicidios en Antioquia (2007–2021)  
- **Fuente:** [Datos Abiertos de Colombia](https://www.datos.gov.co/api/v3/views/db67-sbus/query.json)  
- **Formato:** JSON (descargado vía API REST)  

**Campos principales:**
| Campo | Descripción |
|--------|--------------|
| `Anio` | Año del reporte |
| `NombreRegion` | Subregión del departamento |
| `NombreMunicipio` | Municipio donde ocurrió el evento |
| `NumeroCasos` | Total de suicidios reportados |
| `NumeroPoblacionObjetivo` | Población total del municipio (cuando aplica) |


## ⚙️ Ejecución del Proyecto con Spark (Python)

Sigue estos pasos para ejecutar el procesamiento batch en el entorno local utilizando **Apache Spark** y **Python**.

### 🧾 Requisitos previos
- Tener instalado **Python 3.8 o superior**.  
- Tener instalado **Apache Spark** y configuradas las variables de entorno (`SPARK_HOME` y `PATH`).  
- Tener instalado **Java 8 o superior**.  

Puedes verificar las versiones ejecutando:
```bash
python --version
spark-submit --version
java -version 
```

1. Clonar el repositorio
```bash
git clone https://github.com/usuario/spark-batch-suicidios.git
```

2. Moverse a la ruta
```bash
cd batch_spark
```

3. Ejecutar el script
```bash
python spark_batch_suicidios.py
```

Una vez ejecutado, el script generará una carpeta con nombre similar a:
output/suicidios_antioquia_batch_20251021_234500/

Dentro encontrarás:

- eda_casos_por_anio.csv → Análisis de casos por año
- eda_casos_por_region.csv → Análisis de casos por región
- eda_causas_mortalidad.csv → Causas de mortalidad más frecuentes


## Ejecución del Streaming con Spark y Kafka

Este proyecto utiliza **Apache Spark Structured Streaming** para procesar datos en tiempo real provenientes de **Kafka**.

### Requisitos previos

1. Tener **Kafka** y **Zookeeper** corriendo en tu máquina virtual.

2. Tener **Python 3.x** y las librerías necesarias instaladas:

   ```bash
   pip install pyspark kafka-python
   ```

3. Asegúrate de que el tópico suicidios_data exista en Kafka:

   ```bash
   kafka-topics.sh --create --topic suicidios_data --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
   ```

## Pasos para ejecutar

1. Ejecutar el productor de datos
Esto generará datos simulados y los enviará al tópico de Kafka:

   ```bash
   python3 kafka_producer.py

   ```
Deja esta terminal abierta para que los datos se envíen continuamente.

2. Ejecutar el consumidor de Spark Streaming
En otra terminal, ejecuta el script de Spark:

   ```bash
   spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.7 spark_streaming_consumer.py
   ```
- Esto leerá los datos del tópico suicidios_data.
- Calculará estadísticas por país y género cada 1 minuto.
- Mostrará los resultados en consola.


