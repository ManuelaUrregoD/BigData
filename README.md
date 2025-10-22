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

# 1. Clonar el repositorio
```bash
git clone https://github.com/usuario/spark-batch-suicidios.git
```

# 2. Ejecutar el script
```bash
python spark_batch_suicidios.py
```

Una vez ejecutado, el script generará una carpeta con nombre similar a:
output/suicidios_antioquia_batch_20251021_234500/

Dentro encontrarás:

- eda_casos_por_anio.csv → Análisis de casos por año
- eda_casos_por_region.csv → Análisis de casos por región
- eda_causas_mortalidad.csv → Causas de mortalidad más frecuentes
