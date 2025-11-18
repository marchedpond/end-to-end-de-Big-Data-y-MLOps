# Terraform - Google Cloud Platform

Infraestructura como código para desplegar el pipeline ML en GCP.

## Recursos Creados

- **Cloud Storage Bucket**: Almacenamiento de modelos y datos
- **Pub/Sub Topic**: Streaming de datos (reemplazo de Kafka)
- **Cloud Function**: Endpoint serverless para predicción
- **Service Account**: Cuenta de servicio para Cloud Functions
- **Vertex AI Dataset**: Dataset para entrenamiento (opcional)

## Requisitos Previos

1. Instalar Terraform: https://www.terraform.io/downloads
2. Instalar Google Cloud SDK: https://cloud.google.com/sdk/docs/install
3. Autenticarse en GCP:
   ```bash
   gcloud auth login
   gcloud auth application-default login
   ```

## Uso

### 1. Configurar Variables

```bash
cp terraform.tfvars.example terraform.tfvars
# Editar terraform.tfvars con tus valores
```

### 2. Inicializar Terraform

```bash
terraform init
```

### 3. Planificar Cambios

```bash
terraform plan
```

### 4. Aplicar Infraestructura

```bash
terraform apply
```

### 5. Destruir Infraestructura

```bash
terraform destroy
```

## Configuración del Backend

Para usar un backend remoto (recomendado para producción):

1. Crear bucket para estado:
   ```bash
   gsutil mb gs://ml-pipeline-terraform-state
   ```

2. El backend está configurado en `main.tf`:
   ```hcl
   backend "gcs" {
     bucket = "ml-pipeline-terraform-state"
     prefix = "terraform/state"
   }
   ```

## Outputs

Después de `terraform apply`, verás:
- URL del Cloud Function
- Nombre del bucket
- Topic de Pub/Sub
- Service Account email

