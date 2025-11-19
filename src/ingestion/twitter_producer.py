"""
Productor de datos para Kafka/Pub/Sub
Lee datos del dataset y los envía al stream
"""

import json
import time
import pandas as pd
from kafka import KafkaProducer
from typing import Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TwitterStreamProducer:
    """Productor que lee del dataset y envía a Kafka"""
    
    def __init__(self, 
                 bootstrap_servers: str = "localhost:9092",
                 topic: str = "twitter-stream"):
        """
        Inicializa el productor
        
        Args:
            bootstrap_servers: Servidores de Kafka
            topic: Tópico de Kafka
        """
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self.producer = None
        
    def connect(self):
        """Conecta al broker de Kafka"""
        try:
            self.producer = KafkaProducer(
                bootstrap_servers=self.bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                key_serializer=lambda k: k.encode('utf-8') if k else None
            )
            logger.info(f"Conectado a Kafka en {self.bootstrap_servers}")
        except Exception as e:
            logger.error(f"Error conectando a Kafka: {e}")
            raise
    
    def send_tweet(self, tweet_data: dict):
        """
        Envía un tweet a Kafka
        
        Args:
            tweet_data: Diccionario con datos del tweet
        """
        try:
            tweet_id = tweet_data.get("id", f"tweet_{int(time.time() * 1000)}")
            future = self.producer.send(
                self.topic,
                key=tweet_id,
                value=tweet_data
            )
            logger.debug(f"Tweet enviado: {tweet_id}")
        except Exception as e:
            logger.error(f"Error enviando tweet: {e}")
    
    def stream_from_dataset(self, 
                           dataset_path: str,
                           interval: float = 0.1,
                           limit: Optional[int] = None):
        """
        Lee del dataset CSV y envía a Kafka
        
        Args:
            dataset_path: Ruta al archivo CSV del dataset
            interval: Intervalo entre mensajes en segundos
            limit: Número máximo de registros a enviar (None para todos)
        """
        if not self.producer:
            self.connect()
        
        logger.info(f"Leyendo dataset desde {dataset_path}")
        
        # Leer dataset
        df = pd.read_csv(dataset_path)
        
        if limit:
            df = df.head(limit)
        
        logger.info(f"Enviando {len(df)} tweets...")
        
        sent_count = 0
        try:
            for idx, row in df.iterrows():
                tweet = {
                    "id": f"tweet_{idx}",
                    "text": str(row["sentence"]),
                    "sentiment_label": "positive" if row["sentiment"] == 1 else "negative",
                    "sentiment": row["sentiment"],
                    "timestamp": pd.Timestamp.now().isoformat()
                }
                
                self.send_tweet(tweet)
                sent_count += 1
                
                if sent_count % 100 == 0:
                    logger.info(f"Tweets enviados: {sent_count}/{len(df)}")
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            logger.info("Streaming detenido por el usuario")
        finally:
            self.close()
            logger.info(f"Total de tweets enviados: {sent_count}")
    
    def close(self):
        """Cierra la conexión"""
        if self.producer:
            self.producer.close()
            logger.info("Conexión cerrada")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Twitter Stream Producer")
    parser.add_argument("--dataset", default="data/raw/train_data.csv", help="Ruta al dataset CSV")
    parser.add_argument("--bootstrap-servers", default="localhost:9092", help="Kafka bootstrap servers")
    parser.add_argument("--topic", default="twitter-stream", help="Kafka topic")
    parser.add_argument("--interval", type=float, default=0.1, help="Intervalo entre tweets")
    parser.add_argument("--limit", type=int, default=None, help="Límite de tweets a enviar")
    
    args = parser.parse_args()
    
    producer = TwitterStreamProducer(
        bootstrap_servers=args.bootstrap_servers,
        topic=args.topic
    )
    
    producer.stream_from_dataset(
        dataset_path=args.dataset,
        interval=args.interval,
        limit=args.limit
    )

