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
