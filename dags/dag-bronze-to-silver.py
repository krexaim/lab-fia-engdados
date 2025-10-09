import airflow
from airflow import DAG
from airflow.operators.python import PythonOperator

from kafka import KafkaConsumer
import json
from pathlib import Path
import boto3
from botocore.client import Config
import pandas as pd
from datetime import datetime, timedelta
import io

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, trim, upper
from delta.tables import DeltaTable
from delta import configure_spark_with_delta_pip

import urllib.parse

aws_access_key_id="admin"
aws_secret_access_key="minioadmin"

# --------------------------------------------------------------------
# CONFIGURAÇÕES GERAIS
# --------------------------------------------------------------------
MINIO_ENDPOINT = "http://minio:9000"
MINIO_ACCESS_KEY = "admin"
MINIO_SECRET_KEY = "minioadmin"
# KAFKA_BROKER = "kafka-broker:29092"
# KAFKA_TOPIC = "sink-raw"

BRONZE_PATH = "s3a://raw/"
SILVER_PATH = "s3a://trusted/movies/"



def push_data_to_silver_layer(file_path):

      # Inicia a sessão Spark
    builder  = (
        SparkSession.builder.appName("BronzeToSilverAirflow")
        # Adiciona os pacotes necessários
       .config(
            "spark.jars",
            "/opt/spark/jars/hadoop-aws-3.3.4.jar,/opt/spark/jars/aws-java-sdk-bundle-1.12.262.jar"
        )
        .config("spark.hadoop.fs.s3a.endpoint", MINIO_ENDPOINT)
        .config("spark.hadoop.fs.s3a.access.key", MINIO_ACCESS_KEY)
        .config("spark.hadoop.fs.s3a.secret.key", MINIO_SECRET_KEY)
        .config("spark.hadoop.fs.s3a.path.style.access", "true")
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") 
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") 
        
    )

    spark = configure_spark_with_delta_pip(builder).getOrCreate()

    # Lê o CSV com PySpark
    df = spark.read.option("header", True).csv(file_path)

   # Faz uma limpeza simples
    df_clean = (
        df.dropDuplicates(["show_id"])
            .withColumn("title", trim(col("title")))
            .withColumn("type", upper(col("type")))
            .withColumn("country", upper(col("country")))
            .na.drop(subset=["title", "type", "country"])
    )

    print("Dados limpos, salvando na camada Silver...")

   # ----------------------------------------------------------------
    # Faz o UPSERT (MERGE INTO) na tabela Delta Lake
    # ----------------------------------------------------------------
    try:
        delta_table = DeltaTable.forPath(spark, SILVER_PATH)
        print("Tabela Delta existente — aplicando MERGE (upsert)")

        (
            delta_table.alias("t")
            .merge(
                df_clean.alias("s"),
                "t.show_id = s.show_id"
            )
            .whenMatchedUpdateAll()
            .whenNotMatchedInsertAll()
            .execute()
        )

    except Exception as e:
        print(f"Nenhuma tabela Delta existente. Criando nova. Detalhe: {e}")
        df_clean.write.format("delta").mode("overwrite").save(SILVER_PATH)
        
    print(f"Dados atualizados com sucesso na camada Silver Delta: {SILVER_PATH}")
    spark.stop()
    

dag = DAG(
    dag_id = "silver-layer-processing",
    default_args = {
        "owner": "Fia",
        "start_date" : airflow.utils.dates.days_ago(1),
    },
    schedule_interval = "@yearly",
    catchup = False
)

start = PythonOperator(
    task_id = "start",
    python_callable = lambda: print("Jobs Started"),
    dag=dag
)

move_data_to_silver = PythonOperator(
    task_id='move-data-to-silver',
    python_callable=push_data_to_silver_layer,
    op_args=[BRONZE_PATH],
    dag=dag
)

end = PythonOperator(
    task_id="end",
    python_callable = lambda: print("Jobs completed successfully"),
    dag=dag
)

start >> move_data_to_silver >> end