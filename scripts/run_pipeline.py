#!/usr/bin/env python3
"""
Script principal para ejecutar el pipeline completo
"""

import os
import sys
import argparse

# Agregar ruta del proyecto
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.ingestion.twitter_producer import TwitterStreamProducer
from src.processing.spark_streaming import SparkStreamingProcessor
from src.monitoring.metrics_collector import MetricsCollector
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description="Ejecutar pipeline completo")
    parser.add_argument("--mode", choices=["producer", "processor", "full"], 
                       default="full", help="Modo de ejecución")
    parser.add_argument("--dataset", default="data/raw/train_data.csv")
    parser.add_argument("--bootstrap-servers", default="localhost:9092")
    parser.add_argument("--topic", default="twitter-stream")
    parser.add_argument("--limit", type=int, default=1000, help="Límite de tweets")
    
    args = parser.parse_args()
    
    if args.mode in ["producer", "full"]:
        logger.info("Iniciando productor...")
        producer = TwitterStreamProducer(
            bootstrap_servers=args.bootstrap_servers,
            topic=args.topic
        )
        producer.stream_from_dataset(
            dataset_path=args.dataset,
            interval=0.1,
            limit=args.limit
        )
    
    if args.mode in ["processor", "full"]:
        logger.info("Iniciando procesador...")
        processor = SparkStreamingProcessor()
        try:
            query = processor.start_streaming_pipeline(
                bootstrap_servers=args.bootstrap_servers,
                topic=args.topic,
                output_format="console"
            )
            query.awaitTermination()
        except KeyboardInterrupt:
            logger.info("Deteniendo...")
            query.stop()
            processor.stop()


if __name__ == "__main__":
    main()

