# Infraestructura como Código (IaC)

Este directorio contiene la infraestructura como código para desplegar el pipeline ML en la nube.

## Estructura

```
infrastructure/
├── terraform/
│   └── gcp/              # Terraform para Google Cloud Platform
│       ├── main.tf
│       ├── variables.tf
│       ├── outputs.tf
│       ├── terraform.tfvars.example
│       └── README.md
└── cloudformation/
    └── aws/              # CloudFormation para AWS
        ├── main.yaml
        ├── parameters.json
        └── README.md
```

## Google Cloud Platform (Terraform)

Ver [terraform/gcp/README.md](terraform/gcp/README.md) para instrucciones detalladas.

### Recursos Creados:

- Cloud Storage Bucket
- Pub/Sub Topic y Subscription
- Cloud Function
- Service Account
- Vertex AI Dataset (opcional)

### Uso Rápido:

```bash
cd terraform/gcp
cp terraform.tfvars.example terraform.tfvars
# Editar terraform.tfvars
terraform init
terraform plan
terraform apply
```

## Amazon Web Services (CloudFormation)

Ver [cloudformation/aws/README.md](cloudformation/aws/README.md) para instrucciones detalladas.

### Recursos Creados:

- S3 Bucket
- Lambda Function
- API Gateway
- IAM Roles
- MSK Cluster (opcional)
- EMR Cluster (opcional)

### Uso Rápido:

```bash
cd cloudformation/aws
# Editar parameters.json
aws cloudformation create-stack \
  --stack-name ml-pipeline-infrastructure \
  --template-body file://main.yaml \
  --parameters file://parameters.json \
  --capabilities CAPABILITY_NAMED_IAM
```

## Comparación

| Característica | Terraform (GCP)      | CloudFormation (AWS)   |
| -------------- | -------------------- | ---------------------- |
| Lenguaje       | HCL                  | YAML/JSON              |
| Estado         | Backend remoto (GCS) | CloudFormation service |
| Recursos       | GCP nativos          | AWS nativos            |
| Complejidad    | Media                | Media                  |

## Próximos Pasos

1. Elegir proveedor (GCP o AWS)
2. Configurar credenciales
3. Ajustar variables/parámetros
4. Desplegar infraestructura
5. Subir código de aplicación
6. Probar endpoints
