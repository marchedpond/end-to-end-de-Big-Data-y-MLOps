"""
Endpoint serverless para predicción de sentimiento
Compatible con Google Cloud Functions y AWS Lambda
"""

import json
import os
import sys
from typing import Dict, Any
import logging

# Agregar ruta del proyecto
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Modelo global (se carga una vez)
_model = None


def load_model(model_path: str):
    """Carga el modelo"""
    global _model
    
    if _model is None:
        try:
            from pyspark.ml import PipelineModel
            from pyspark.sql import SparkSession
            
            logger.info(f"Cargando modelo desde {model_path}")
            
            # Crear sesión Spark
            spark = SparkSession.builder \
                .appName("SentimentEndpoint") \
                .master("local[*]") \
                .getOrCreate()
            
            # Cargar modelo
            _model = PipelineModel.load(model_path)
            logger.info("Modelo cargado exitosamente")
        except Exception as e:
            logger.error(f"Error cargando modelo: {e}")
            raise


def predict_sentiment(text: str, model_path: str = None) -> Dict[str, Any]:
    """
    Predice el sentimiento de un texto
    
    Args:
        text: Texto a analizar
        model_path: Ruta al modelo (si no está cargado)
    
    Returns:
        Diccionario con predicción
    """
    global _model
    
    if _model is None and model_path:
        load_model(model_path)
    
    if _model is None:
        return {
            "text": text,
            "sentiment": "error",
            "status": "error",
            "error": "Modelo no cargado"
        }
    
    try:
        from pyspark.sql import SparkSession
        
        spark = SparkSession.builder.getOrCreate()
        
        # Crear DataFrame con el texto
        from pyspark.sql import Row
        data = [Row(cleaned_text=text)]
        df = spark.createDataFrame(data)
        
        # Predecir
        predictions = _model.transform(df)
        prediction = predictions.select("prediction").first()[0]
        
        # Convertir a etiqueta
        sentiment_map = {0.0: "negative", 1.0: "positive"}
        sentiment = sentiment_map.get(prediction, "neutral")
        
        return {
            "text": text,
            "sentiment": sentiment,
            "status": "success"
        }
    except Exception as e:
        logger.error(f"Error en predicción: {e}")
        return {
            "text": text,
            "sentiment": "error",
            "status": "error",
            "error": str(e)
        }


# Google Cloud Functions
def gcp_sentiment_endpoint(request):
    """Endpoint para Google Cloud Functions"""
    model_path = os.environ.get("MODEL_PATH", "data/models/sentiment_model")
    load_model(model_path)
    
    if request.method == "POST":
        request_json = request.get_json(silent=True)
        text = request_json.get("text", "") if request_json else ""
    else:
        text = request.args.get("text", "")
    
    if not text:
        return json.dumps({"error": "Parámetro 'text' requerido"}), 400
    
    result = predict_sentiment(text, model_path)
    return json.dumps(result), 200, {"Content-Type": "application/json"}


# AWS Lambda
def lambda_handler(event, context):
    """Handler para AWS Lambda"""
    model_path = os.environ.get("MODEL_PATH", "data/models/sentiment_model")
    load_model(model_path)
    
    if isinstance(event, str):
        event = json.loads(event)
    
    text = event.get("text", "") or event.get("body", {}).get("text", "")
    
    if not text:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Parámetro 'text' requerido"})
        }
    
    result = predict_sentiment(text, model_path)
    
    return {
        "statusCode": 200,
        "body": json.dumps(result)
    }


# Flask app para testing local
def create_flask_app(model_path: str = "data/models/sentiment_model"):
    """Crea app Flask para testing"""
    from flask import Flask, request, jsonify
    
    app = Flask(__name__)
    load_model(model_path)
    
    @app.route("/predict", methods=["GET", "POST"])
    def predict():
        if request.method == "POST":
            data = request.get_json()
            text = data.get("text", "") if data else ""
        else:
            text = request.args.get("text", "")
        
        if not text:
            return jsonify({"error": "Parámetro 'text' requerido"}), 400
        
        result = predict_sentiment(text, model_path)
        return jsonify(result)
    
    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({"status": "healthy", "model_loaded": _model is not None})
    
    return app


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Servidor local")
    parser.add_argument("--model-path", default="data/models/sentiment_model")
    parser.add_argument("--port", type=int, default=8080)
    
    args = parser.parse_args()
    
    app = create_flask_app(args.model_path)
    app.run(host="0.0.0.0", port=args.port, debug=True)

