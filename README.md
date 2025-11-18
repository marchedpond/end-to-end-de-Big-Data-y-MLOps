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
├── infrastructure/
│   ├── terraform/
│   │   └── gcp/              # Terraform para GCP
│   │       ├── main.tf
│   │       ├── variables.tf
│   │       ├── outputs.tf
│   │       └── terraform.tfvars.example
│   └── cloudformation/
│       └── aws/              # CloudFormation para AWS
│           ├── main.yaml
│           └── parameters.json
└── README.md
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

## Requisitos Previos

### Para GCP:

- Terraform >= 1.0
- Google Cloud SDK
- Cuenta de GCP con proyecto configurado

### Para AWS:

- AWS CLI
- Credenciales AWS configuradas
- Permisos para crear recursos

## Documentación

### Infraestructura
- [Infraestructura GCP](infrastructure/terraform/gcp/README.md)
- [Infraestructura AWS](infrastructure/cloudformation/aws/README.md)
- [README General de Infraestructura](infrastructure/README.md)

### Análisis y Estrategias
- [Comparación de Costos y Rendimiento GCP vs AWS](docs/COMPARACION_COSTOS_RENDIMIENTO.md)
- [Estrategia de Calidad de Datos en Streaming](docs/ESTRATEGIA_CALIDAD_DATOS_STREAMING.md)
- [Análisis de Cumplimiento de Requisitos](ANALISIS_REQUISITOS.md)

## Licencia

Este proyecto es para fines educativos.
