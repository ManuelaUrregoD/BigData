import os
import json
import requests
from datetime import datetime
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, avg

# --- Configuración ---
API_URL = "https://www.datos.gov.co/api/views/db67-sbus/rows.json?accessType=DOWNLOAD"
TMP_JSON = "/tmp/suicidios_antioquia.json"
OUTPUT_DIR = f"./output/suicidios_antioquia_batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
os.makedirs(OUTPUT_DIR, exist_ok=True)

print(f"OUTPUT_DIR = {OUTPUT_DIR}")

# --- Descargar datos ---
print(f"Descargando datos desde: {API_URL}")
try:
    resp = requests.get(API_URL)
    resp.raise_for_status()
    with open(TMP_JSON, "w", encoding="utf-8") as f:
        f.write(resp.text)
    print("✅ Descarga completada correctamente.")
except requests.RequestException as e:
    print(f"❌ Error HTTP al descargar datos: {e}")

# --- Iniciar Spark ---
spark = SparkSession.builder.appName("BatchSuicidiosAntioquia").getOrCreate()
print("Spark iniciado.")

# --- Leer el JSON completo ---
with open(TMP_JSON, "r", encoding="utf-8") as f:
    raw_json = json.load(f)

# Extraer nombres de columnas y datos
columns = [col["name"] for col in raw_json["meta"]["view"]["columns"]]
data = raw_json["data"]

# Limpiar datos
cleaned_data = [[str(x) if x is not None else "" for x in row] for row in data]

# Crear DataFrame
df = spark.createDataFrame(cleaned_data, schema=columns)
for c in df.columns:
    df = df.withColumnRenamed(c, c.strip().replace(" ", "_").lower())

print("✅ DataFrame creado con esquema correcto.")
df.printSchema()
df.show(5, truncate=False)

# --- Conversión de columnas numéricas ---
df = df.withColumn("anio", col("anio").cast("int"))
df = df.withColumn("numeropoblacionobjetivo", col("numeropoblacionobjetivo").cast("int"))
df = df.withColumn("numerocasos", col("numerocasos").cast("int"))

# --- 🔍 Análisis Exploratorio (EDA) ---

# Total de casos registrados
total_casos = df.agg({"numerocasos": "sum"}).collect()[0][0]
print(f"\n📊 Total de casos registrados: {total_casos}")

# Casos por año
eda_anio = df.groupBy("anio").agg(count("*").alias("registros"), 
                                  avg("numerocasos").alias("promedio_casos"))
print("\n📈 Casos por año:")
eda_anio.show()

# Casos por región
eda_region = df.groupBy("nombreregion").agg(count("*").alias("registros"),
                                            avg("numerocasos").alias("promedio_casos"))
print("\n🌎 Casos por región:")
eda_region.show()

# Causas más comunes
eda_causas = df.groupBy("causamortalidad").agg(count("*").alias("frecuencia")).orderBy(col("frecuencia").desc())
print("\n⚰️ Causas de mortalidad más frecuentes:")
eda_causas.show(10)

# --- 💾 Guardar resultados procesados ---
output_clean = os.path.join(OUTPUT_DIR, "dataset_limpio.parquet")
output_anio = os.path.join(OUTPUT_DIR, "eda_casos_por_anio.csv")
output_region = os.path.join(OUTPUT_DIR, "eda_casos_por_region.csv")
output_causas = os.path.join(OUTPUT_DIR, "eda_causas_mortalidad.csv")

# Guardar dataset limpio
df.write.mode("overwrite").parquet(output_clean)

# Guardar EDA (coalesce(1) para un solo CSV por análisis)
eda_anio.coalesce(1).write.mode("overwrite").option("header", True).csv(output_anio)
eda_region.coalesce(1).write.mode("overwrite").option("header", True).csv(output_region)
eda_causas.coalesce(1).write.mode("overwrite").option("header", True).csv(output_causas)

print("\n✅ Resultados procesados guardados en:")
print(f"   • Dataset limpio: {output_clean}")
print(f"   • Casos por año: {output_anio}")
print(f"   • Casos por región: {output_region}")
print(f"   • Causas más comunes: {output_causas}")

spark.stop()
