# Requerimientos del Proyecto

## Dataset

### Sentiment140 Dataset

**Fuente:** Kaggle  
**Link:** https://www.kaggle.com/datasets/kazanova/sentiment140

**Descripción:**

- Dataset de análisis de sentimiento con 1.6 millones de tweets
- Etiquetas: 0 (negativo) y 1 (positivo)
- Formato: CSV con columnas `sentence` y `sentiment`

**Archivos incluidos:**

- `train_data.csv`: Dataset de entrenamiento (~1.5M registros)
- `test_data.csv`: Dataset de prueba
- `vocab.json`: Vocabulario preprocesado
- `vocab.py`: Script de procesamiento de vocabulario
- `Exploring Data.ipynb`: Notebook de exploración

**Ubicación en el proyecto:**

```
data/raw/
├── train_data.csv
├── test_data.csv
├── vocab.json
├── vocab.py
└── Exploring Data.ipynb
```

## Herramientas Requeridas

### Infraestructura

- **Terraform** >= 1.0 (para GCP)
- **AWS CLI** (para CloudFormation)
- **Python** 3.8+

### Librerías Python (si se implementa código de aplicación)

- pandas
- numpy
- scikit-learn
- pyspark (para procesamiento distribuido)
- kafka-python (para ingesta de datos)

## Credenciales Cloud

### Google Cloud Platform

- Cuenta de GCP
- Proyecto configurado
- Credenciales de servicio o `gcloud auth`

### Amazon Web Services

- Cuenta de AWS
- Credenciales configuradas (`aws configure`)
- Permisos para crear recursos

## Notas

- El dataset debe descargarse manualmente desde Kaggle
- Requiere cuenta de Kaggle para descargar
- El archivo `archive.zip` contiene todos los archivos del dataset
