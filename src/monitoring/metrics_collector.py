"""
Colector de métricas para monitoreo del pipeline
"""

import time
import json
from datetime import datetime
from typing import Dict, List, Optional
from collections import defaultdict, deque
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MetricsCollector:
    """Colector de métricas"""
    
    def __init__(self):
        """Inicializa el colector"""
        self.metrics = {
            "tweets_processed": 0,
            "predictions_made": 0,
            "errors": 0,
            "latency_sum": 0.0,
            "latency_count": 0,
            "sentiment_distribution": defaultdict(int),
            "accuracy_sum": 0.0,
            "accuracy_count": 0
        }
        
        self.recent_predictions = deque(maxlen=100)
        self.recent_errors = deque(maxlen=50)
    
    def record_tweet_processed(self):
        """Registra un tweet procesado"""
        self.metrics["tweets_processed"] += 1
    
    def record_prediction(self, 
                         text: str,
                         predicted_sentiment: str,
                         actual_sentiment: Optional[str] = None,
                         latency: float = 0.0):
        """Registra una predicción"""
        self.metrics["predictions_made"] += 1
        self.metrics["latency_sum"] += latency
        self.metrics["latency_count"] += 1
        self.metrics["sentiment_distribution"][predicted_sentiment] += 1
        
        if actual_sentiment:
            is_correct = (predicted_sentiment == actual_sentiment)
            self.metrics["accuracy_sum"] += (1.0 if is_correct else 0.0)
            self.metrics["accuracy_count"] += 1
        
        self.recent_predictions.append({
            "timestamp": datetime.now().isoformat(),
            "text": text[:100],
            "predicted": predicted_sentiment,
            "actual": actual_sentiment,
            "latency": latency
        })
    
    def record_error(self, error_type: str, error_message: str):
        """Registra un error"""
        self.metrics["errors"] += 1
        self.recent_errors.append({
            "timestamp": datetime.now().isoformat(),
            "type": error_type,
            "message": error_message
        })
    
    def get_metrics_summary(self) -> Dict:
        """Obtiene resumen de métricas"""
        avg_latency = (
            self.metrics["latency_sum"] / self.metrics["latency_count"]
            if self.metrics["latency_count"] > 0
            else 0.0
        )
        
        accuracy = (
            self.metrics["accuracy_sum"] / self.metrics["accuracy_count"]
            if self.metrics["accuracy_count"] > 0
            else None
        )
        
        return {
            "tweets_processed": self.metrics["tweets_processed"],
            "predictions_made": self.metrics["predictions_made"],
            "errors": self.metrics["errors"],
            "average_latency_seconds": round(avg_latency, 4),
            "accuracy": round(accuracy, 4) if accuracy is not None else None,
            "sentiment_distribution": dict(self.metrics["sentiment_distribution"]),
            "recent_predictions_count": len(self.recent_predictions),
            "recent_errors_count": len(self.recent_errors)
        }
    
    def export_metrics(self, filepath: str):
        """Exporta métricas a JSON"""
        export_data = {
            "timestamp": datetime.now().isoformat(),
            "summary": self.get_metrics_summary(),
            "recent_predictions": list(self.recent_predictions),
            "recent_errors": list(self.recent_errors)
        }
        
        with open(filepath, "w") as f:
            json.dump(export_data, f, indent=2)
        
        logger.info(f"Métricas exportadas a {filepath}")


class PredictionTimer:
    """Context manager para medir latencia"""
    
    def __init__(self, metrics_collector: MetricsCollector):
        self.metrics_collector = metrics_collector
        self.start_time = None
    
    def __enter__(self):
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        latency = time.time() - self.start_time
        if exc_type:
            self.metrics_collector.record_error(
                error_type=exc_type.__name__,
                error_message=str(exc_val)
            )
        return False
    
    def get_latency(self) -> float:
        """Obtiene la latencia"""
        if self.start_time:
            return time.time() - self.start_time
        return 0.0

