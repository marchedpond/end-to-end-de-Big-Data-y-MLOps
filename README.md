# Pipeline ML - Infraestructura como Código

Infraestructura como código para desplegar un pipeline de ML en la nube usando Terraform (GCP) y CloudFormation (AWS).

## Arquitectura

```
Twitter Stream → Kafka/Pub/Sub → Spark Streaming → Modelo ML → Endpoint → Monitoreo
```

## Infraestructura

Este proyecto contiene la infraestructura como código para:

- **Google Cloud Platform**: Terraform
- **Amazon Web Services**: CloudFormation

## Estructura del Proyecto

```
.
├── src/                       # Código de aplicación
│   ├── ingestion/            # Ingesta de datos (Kafka producer)
│   ├── processing/           # Procesamiento con Spark Streaming
│   ├── training/             # Entrenamiento del modelo
│   ├── deployment/           # Endpoint (Cloud Functions/Lambda)
│   └── monitoring/           # Monitoreo y métricas
├── infrastructure/
│   ├── terraform/
│   │   └── gcp/              # Terraform para GCP
│   └── cloudformation/
│       └── aws/              # CloudFormation para AWS
├── data/                     # Datos y modelos
│   ├── raw/                  # Dataset original
│   ├── processed/            # Datos procesados
│   └── models/               # Modelos entrenados
├── scripts/                  # Scripts de utilidad
└── docs/                     # Documentación
```

## Uso Rápido

### Google Cloud Platform (Terraform)

```bash
cd infrastructure/terraform/gcp
cp terraform.tfvars.example terraform.tfvars
# Editar terraform.tfvars con tus valores
terraform init
terraform plan
terraform apply
```

### Amazon Web Services (CloudFormation)

```bash
cd infrastructure/cloudformation/aws
# Editar parameters.json con tus valores
aws cloudformation create-stack \
  --stack-name ml-pipeline-infrastructure \
  --template-body file://main.yaml \
  --parameters file://parameters.json \
  --capabilities CAPABILITY_NAMED_IAM
```

## Recursos Creados

### GCP (Terraform)

- Cloud Storage Bucket
- Pub/Sub Topic y Subscription
- Cloud Function
- Service Account
- Vertex AI Dataset (opcional)

### AWS (CloudFormation)

- S3 Bucket
- Lambda Function
- API Gateway
- IAM Roles
- MSK Cluster (opcional)
- EMR Cluster (opcional)

## Nota Importante

**Este proyecto incluye infraestructura como código para ambas plataformas (GCP y AWS), pero NO es necesario desplegar en ambas.** La comparativa de costos y rendimiento se realiza como investigación/documentación (ver `docs/COMPARACION_COSTOS_RENDIMIENTO.md`).

## Instalación

```bash
# Instalar dependencias Python
pip install -r requirements.txt

# Instalar Java (requerido para Spark)
# macOS: brew install openjdk@11
# Linux: sudo apt-get install openjdk-11-jdk
```

## Uso

### 1. Entrenar Modelo

```bash
python src/training/train_model.py \
    --data-path data/raw/train_data.csv \
    --model-path data/models/sentiment_model
```

### 2. Ejecutar Pipeline Completo

```bash
# Requiere Kafka corriendo
python scripts/run_pipeline.py --mode full --limit 1000
```

### 3. Probar Endpoint Local

```bash
python src/deployment/cloud_function.py \
    --model-path data/models/sentiment_model \
    --port 8080
```

### 4. Dashboard de Monitoreo

```bash
python src/monitoring/dashboard.py --port 8080
```

## Requisitos Previos

### Para Infraestructura:

- Terraform >= 1.0 (para GCP)
- AWS CLI (para AWS)
- Google Cloud SDK (opcional, para GCP)
- Credenciales cloud (opcional, para desplegar)

### Para Código de Aplicación:

- Python 3.8+
- Java 8 o 11 (para Spark)
- Apache Kafka (para streaming)

## Documentación

### Infraestructura

- [Infraestructura GCP](infrastructure/terraform/gcp/README.md)
- [Infraestructura AWS](infrastructure/cloudformation/aws/README.md)
- [README General de Infraestructura](infrastructure/README.md)

### Análisis y Estrategias

- [Comparación de Costos y Rendimiento GCP vs AWS](docs/COMPARACION_COSTOS_RENDIMIENTO.md)
- [Estrategia de Calidad de Datos en Streaming](docs/ESTRATEGIA_CALIDAD_DATOS_STREAMING.md)

## Licencia

Este proyecto es para fines educativos.
