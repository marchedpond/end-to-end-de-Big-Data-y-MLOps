"""
Entrenamiento del modelo de clasificación de sentimiento
Usa PySpark ML para entrenar el modelo
"""

import os
from pyspark.sql import SparkSession
from pyspark.ml import Pipeline
from pyspark.ml.feature import (
    Tokenizer, StopWordsRemover, CountVectorizer, IDF, StringIndexer
)
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.sql.functions import col
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SentimentModelTrainer:
    """Entrenador del modelo de sentimiento"""
    
    def __init__(self, 
                 app_name: str = "SentimentModelTraining",
                 master: str = "local[*]"):
        """Inicializa el entrenador"""
        self.app_name = app_name
        self.master = master
        self.spark = None
        self.model = None
        
    def create_spark_session(self):
        """Crea la sesión de Spark"""
        self.spark = SparkSession.builder \
            .appName(self.app_name) \
            .master(self.master) \
            .getOrCreate()
        
        self.spark.sparkContext.setLogLevel("WARN")
        logger.info(f"Sesión Spark creada: {self.app_name}")
    
    def create_feature_pipeline(self):
        """Crea el pipeline de características"""
        tokenizer = Tokenizer(inputCol="cleaned_text", outputCol="words")
        stop_words = StopWordsRemover(
            inputCol="words",
            outputCol="filtered_words"
        )
        count_vectorizer = CountVectorizer(
            inputCol="filtered_words",
            outputCol="raw_features",
            vocabSize=1000,
            minDF=2.0
        )
        idf = IDF(inputCol="raw_features", outputCol="features")
        label_indexer = StringIndexer(
            inputCol="sentiment",
            outputCol="label"
        )
        
        feature_pipeline = Pipeline(stages=[
            tokenizer,
            stop_words,
            count_vectorizer,
            idf,
            label_indexer
        ])
        
        return feature_pipeline
    
    def train_model(self, 
                   training_data_path: str,
                   model_path: str,
                   test_size: float = 0.2):
        """
        Entrena el modelo
        
        Args:
            training_data_path: Ruta a los datos de entrenamiento
            model_path: Ruta donde guardar el modelo
            test_size: Proporción de datos para test
        """
        if not self.spark:
            self.create_spark_session()
        
        logger.info(f"Cargando datos desde {training_data_path}")
        
        # Cargar datos
        df = self.spark.read.csv(training_data_path, header=True, inferSchema=True)
        
        # Preparar datos (asumiendo que ya tienen cleaned_text)
        # Si no, necesitaríamos limpiar primero
        df = df.filter(col("sentence").isNotNull()) \
               .filter(col("sentiment").isNotNull())
        
        # Renombrar columnas si es necesario
        if "sentence" in df.columns and "cleaned_text" not in df.columns:
            from pyspark.sql.functions import regexp_replace, lower
            df = df.withColumn(
                "cleaned_text",
                regexp_replace(lower(col("sentence")), r'[^a-zA-Z\s]', '')
            )
        
        logger.info(f"Datos cargados: {df.count()} registros")
        
        # Dividir en train/test
        train_df, test_df = df.randomSplit([1.0 - test_size, test_size], seed=42)
        
        logger.info(f"Train: {train_df.count()}, Test: {test_df.count()}")
        
        # Crear pipeline
        feature_pipeline = self.create_feature_pipeline()
        feature_model = feature_pipeline.fit(train_df)
        
        # Transformar datos
        train_features = feature_model.transform(train_df)
        test_features = feature_model.transform(test_df)
        
        # Entrenar modelo
        classifier = LogisticRegression(
            maxIter=100,
            regParam=0.01,
            featuresCol="features",
            labelCol="label"
        )
        
        logger.info("Entrenando modelo...")
        model = classifier.fit(train_features)
        
        # Evaluar
        predictions = model.transform(test_features)
        
        evaluator = MulticlassClassificationEvaluator(
            labelCol="label",
            predictionCol="prediction",
            metricName="accuracy"
        )
        
        accuracy = evaluator.evaluate(predictions)
        logger.info(f"Accuracy: {accuracy:.4f}")
        
        # Guardar pipeline completo
        self.model = Pipeline(stages=feature_pipeline.getStages() + [model])
        full_model = self.model.fit(train_df)
        
        os.makedirs(model_path, exist_ok=True)
        logger.info(f"Guardando modelo en {model_path}")
        full_model.write().overwrite().save(model_path)
        logger.info("Modelo guardado exitosamente")
        
        return accuracy
    
    def stop(self):
        """Detiene la sesión"""
        if self.spark:
            self.spark.stop()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Entrenar modelo")
    parser.add_argument("--data-path", required=True, help="Ruta a los datos")
    parser.add_argument("--model-path", required=True, help="Ruta donde guardar el modelo")
    
    args = parser.parse_args()
    
    trainer = SentimentModelTrainer()
    
    try:
        accuracy = trainer.train_model(
            training_data_path=args.data_path,
            model_path=args.model_path
        )
        print(f"\nModelo entrenado! Accuracy: {accuracy:.4f}")
    finally:
        trainer.stop()

