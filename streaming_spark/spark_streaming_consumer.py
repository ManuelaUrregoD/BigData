from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, window, avg, sum
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, TimestampType

# Crear sesión de Spark
spark = SparkSession.builder \
    .appName("StreamingSuicidiosKafkaSpark") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# Esquema de los datos JSON
esquema = StructType([
    StructField("pais", StringType()),
    StructField("anio", IntegerType()),
    StructField("genero", StringType()),
    StructField("numero_suicidios", IntegerType()),
    StructField("poblacion", IntegerType()),
    StructField("marca_tiempo", TimestampType())
])

# Leer flujo desde Kafka
datos_kafka = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "suicidios_data") \
    .option("startingOffsets", "latest") \
    .load()

# Parsear JSON
datos_parseados = datos_kafka.select(from_json(col("value").cast("string"), esquema).alias("data")).select("data.*")

# Calcular estadísticas por país y género cada 1 minuto
estadisticas_ventana = datos_parseados \
    .groupBy(window(col("marca_tiempo"), "1 minute"), col("pais"), col("genero")) \
    .agg(
        sum("numero_suicidios").alias("total_suicidios"),
        avg("poblacion").alias("promedio_poblacion")
    )

# Mostrar resultados en consola
consulta = estadisticas_ventana.writeStream \
    .outputMode("complete") \
    .format("console") \
    .option("truncate", "false") \
    .start()

consulta.awaitTermination()
