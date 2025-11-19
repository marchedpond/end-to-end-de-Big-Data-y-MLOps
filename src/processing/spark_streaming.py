"""
Procesamiento con Spark Streaming
Lee de Kafka, procesa y limpia los datos
"""

import re
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, from_json, udf, length, current_timestamp
)
from pyspark.sql.types import (
    StructType, StructField, StringType, IntegerType
)
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SparkStreamingProcessor:
    """Procesador de streaming con Spark"""
    
    def __init__(self, 
                 app_name: str = "SentimentAnalysisPipeline",
                 master: str = "local[*]",
                 checkpoint_location: str = "data/checkpoints"):
        """
        Inicializa el procesador
        
        Args:
            app_name: Nombre de la aplicación
            master: URL del master de Spark
            checkpoint_location: Ubicación para checkpoints
        """
        self.app_name = app_name
        self.master = master
        self.checkpoint_location = checkpoint_location
        self.spark = None
        
    def create_spark_session(self):
        """Crea la sesión de Spark"""
        self.spark = SparkSession.builder \
            .appName(self.app_name) \
            .master(self.master) \
            .config("spark.sql.streaming.checkpointLocation", self.checkpoint_location) \
            .getOrCreate()
        
        self.spark.sparkContext.setLogLevel("WARN")
        logger.info(f"Sesión Spark creada: {self.app_name}")
    
    def clean_text_udf(self):
        """UDF para limpiar texto"""
        def clean_text(text: str) -> str:
            if not text:
                return ""
            # Remover URLs
            text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
            # Remover menciones y hashtags
            text = re.sub(r'@\w+|#\w+', '', text)
            # Remover caracteres especiales
            text = re.sub(r'[^a-zA-Z\s]', '', text)
            # Minúsculas y espacios
            text = ' '.join(text.lower().split())
            return text
        
        return udf(clean_text, StringType())
    
    def read_from_kafka(self, 
                       bootstrap_servers: str,
                       topic: str,
                       starting_offsets: str = "latest"):
        """Lee datos de Kafka"""
        if not self.spark:
            self.create_spark_session()
        
        logger.info(f"Leyendo de Kafka: {topic}")
        
        df = self.spark \
            .readStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", bootstrap_servers) \
            .option("subscribe", topic) \
            .option("startingOffsets", starting_offsets) \
            .option("failOnDataLoss", "false") \
            .load()
        
        return df
    
    def parse_kafka_message(self, df):
        """Parsea mensajes JSON de Kafka"""
        tweet_schema = StructType([
            StructField("id", StringType(), True),
            StructField("text", StringType(), True),
            StructField("sentiment_label", StringType(), True),
            StructField("sentiment", IntegerType(), True),
            StructField("timestamp", StringType(), True)
        ])
        
        parsed_df = df.select(
            col("key").cast("string").alias("kafka_key"),
            from_json(col("value").cast("string"), tweet_schema).alias("data"),
            col("timestamp").alias("kafka_timestamp")
        ).select(
            col("kafka_key"),
            col("data.*"),
            col("kafka_timestamp")
        )
        
        return parsed_df
    
    def process_tweets(self, df):
        """Procesa y limpia tweets"""
        clean_text = self.clean_text_udf()
        
        processed_df = df \
            .withColumn("cleaned_text", clean_text(col("text"))) \
            .withColumn("text_length", length(col("cleaned_text"))) \
            .filter(col("cleaned_text") != "") \
            .filter(col("text_length") > 3) \
            .withColumn("processing_timestamp", current_timestamp())
        
        return processed_df
    
    def start_streaming_pipeline(self,
                                bootstrap_servers: str,
                                topic: str,
                                output_format: str = "console"):
        """Inicia el pipeline de streaming"""
        if not self.spark:
            self.create_spark_session()
        
        kafka_df = self.read_from_kafka(bootstrap_servers, topic)
        parsed_df = self.parse_kafka_message(kafka_df)
        processed_df = self.process_tweets(parsed_df)
        
        if output_format == "console":
            query = processed_df.writeStream \
                .outputMode("append") \
                .format("console") \
                .option("truncate", "false") \
                .start()
        elif output_format == "memory":
            query = processed_df.writeStream \
                .outputMode("append") \
                .format("memory") \
                .queryName("processed_tweets") \
                .start()
        else:
            raise ValueError(f"Formato no soportado: {output_format}")
        
        logger.info("Pipeline de streaming iniciado")
        return query
    
    def stop(self):
        """Detiene el procesamiento"""
        if self.spark:
            self.spark.stop()
            logger.info("Sesión Spark detenida")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Spark Streaming Processor")
    parser.add_argument("--bootstrap-servers", default="localhost:9092")
    parser.add_argument("--topic", default="twitter-stream")
    parser.add_argument("--output-format", default="console", choices=["console", "memory"])
    
    args = parser.parse_args()
    
    processor = SparkStreamingProcessor()
    
    try:
        query = processor.start_streaming_pipeline(
            bootstrap_servers=args.bootstrap_servers,
            topic=args.topic,
            output_format=args.output_format
        )
        query.awaitTermination()
    except KeyboardInterrupt:
        logger.info("Deteniendo pipeline...")
        query.stop()
        processor.stop()

