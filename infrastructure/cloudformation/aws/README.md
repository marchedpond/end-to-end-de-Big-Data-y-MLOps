# CloudFormation - Amazon Web Services

Infraestructura como código para desplegar el pipeline ML en AWS.

## Recursos Creados

- **S3 Bucket**: Almacenamiento de modelos y datos
- **Lambda Function**: Endpoint serverless para predicción
- **API Gateway**: API REST para invocar Lambda
- **IAM Role**: Rol de ejecución para Lambda
- **MSK Cluster**: (Opcional) Kafka managed service
- **EMR Cluster**: (Opcional) Spark cluster para procesamiento

## Requisitos Previos

1. AWS CLI instalado: https://aws.amazon.com/cli/
2. Credenciales AWS configuradas:
   ```bash
   aws configure
   ```
3. Permisos adecuados para crear recursos

## Uso

### 1. Configurar Parámetros

Editar `parameters.json` con tus valores:
- `BucketName`: Debe ser único globalmente
- `ProjectName`: Nombre del proyecto
- `Environment`: dev, staging, o prod

### 2. Validar Template

```bash
aws cloudformation validate-template \
  --template-body file://main.yaml
```

### 3. Crear Stack

```bash
aws cloudformation create-stack \
  --stack-name ml-pipeline-infrastructure \
  --template-body file://main.yaml \
  --parameters file://parameters.json \
  --capabilities CAPABILITY_NAMED_IAM
```

### 4. Verificar Estado

```bash
aws cloudformation describe-stacks \
  --stack-name ml-pipeline-infrastructure
```

### 5. Ver Outputs

```bash
aws cloudformation describe-stacks \
  --stack-name ml-pipeline-infrastructure \
  --query 'Stacks[0].Outputs'
```

### 6. Eliminar Stack

```bash
aws cloudformation delete-stack \
  --stack-name ml-pipeline-infrastructure
```

## Despliegue con AWS SAM (Alternativa)

Si prefieres usar AWS SAM:

```bash
# Instalar SAM CLI
pip install aws-sam-cli

# Build
sam build

# Deploy
sam deploy --guided
```

## Notas

- El bucket S3 debe tener un nombre único globalmente
- Lambda requiere que el código esté en S3 antes del despliegue
- MSK y EMR están comentados por defecto (costos altos)
- Ajusta los parámetros según tus necesidades

