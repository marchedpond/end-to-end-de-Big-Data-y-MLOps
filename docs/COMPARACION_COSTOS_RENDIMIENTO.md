# Comparación de Costos y Rendimiento: GCP vs AWS

## Resumen Ejecutivo

Este documento compara los costos y rendimiento de desplegar el pipeline ML en Google Cloud Platform (GCP) vs Amazon Web Services (AWS) usando la infraestructura definida en este proyecto.

## Componentes del Pipeline y Costos

### 1. Ingesta de Datos

#### GCP - Pub/Sub
- **Costo**: $0.40 por millón de mensajes
- **Throughput**: Hasta 10,000 mensajes/segundo por tópico
- **Ventajas**: 
  - Integración nativa con Dataflow
  - Auto-scaling automático
  - Retención de mensajes hasta 7 días
- **Costo mensual estimado** (1M tweets/día): ~$12/mes

#### AWS - MSK (Managed Kafka)
- **Costo**: ~$0.10 por hora por broker (kafka.m5.large)
- **Throughput**: Depende del tamaño del cluster
- **Ventajas**:
  - Kafka nativo (compatible 100%)
  - Mayor control sobre configuración
- **Costo mensual estimado** (2 brokers): ~$144/mes

**Ganador**: GCP Pub/Sub (más económico para streaming simple)

### 2. Procesamiento Distribuido

#### GCP - Cloud Dataflow
- **Costo**: 
  - Worker: $0.056/hora (n1-standard-1)
  - Streaming: +20% overhead
- **Ventajas**:
  - Auto-scaling automático
  - Sin gestión de infraestructura
  - Integración con BigQuery, Pub/Sub
- **Costo mensual estimado** (2 workers 24/7): ~$80/mes

#### AWS - EMR (Elastic MapReduce)
- **Costo**:
  - Master: $0.27/hora (m5.xlarge)
  - Core/Task: $0.27/hora (m5.xlarge)
  - Spot instances: ~70% descuento
- **Ventajas**:
  - Control total sobre cluster Spark
  - Spot instances para ahorro
  - Flexibilidad en configuración
- **Costo mensual estimado** (1 master + 2 core, on-demand): ~$195/mes
- **Costo mensual estimado** (con spot): ~$58/mes

**Ganador**: GCP Dataflow (simplicidad) o AWS EMR con spot (costos optimizados)

### 3. Entrenamiento de Modelos

#### GCP - Vertex AI Training
- **Costo**:
  - n1-standard-4: $0.19/hora
  - GPU (V100): $2.48/hora
- **Ventajas**:
  - Hyperparameter tuning integrado
  - AutoML disponible
  - Versionado de modelos
- **Costo mensual estimado** (entrenamiento semanal): ~$50/mes

#### AWS - SageMaker Training
- **Costo**:
  - ml.m5.xlarge: $0.23/hora
  - GPU (p3.2xlarge): $3.06/hora
- **Ventajas**:
  - Amplia gama de instancias
  - Spot training (hasta 90% descuento)
  - Built-in algorithms
- **Costo mensual estimado** (entrenamiento semanal): ~$50/mes

**Ganador**: Empate (costos similares)

### 4. Despliegue de Modelos

#### GCP - Cloud Functions
- **Costo**:
  - Invocaciones: Primeros 2M gratis/mes
  - Después: $0.40 por millón
  - Compute: $0.0000025 por GB-segundo
- **Ventajas**:
  - Serverless, sin gestión
  - Auto-scaling
- **Costo mensual estimado** (100K invocaciones): ~$5/mes

#### AWS - Lambda
- **Costo**:
  - Invocaciones: Primeros 1M gratis/mes
  - Después: $0.20 por millón
  - Compute: $0.0000166667 por GB-segundo
- **Ventajas**:
  - Mayor límite de tiempo (15 min)
  - Más memoria disponible (10GB)
- **Costo mensual estimado** (100K invocaciones): ~$3/mes

**Ganador**: AWS Lambda (ligeramente más económico)

### 5. Almacenamiento

#### GCP - Cloud Storage
- **Costo**:
  - Standard: $0.020/GB/mes
  - Nearline: $0.010/GB/mes
  - Coldline: $0.004/GB/mes
- **Costo mensual estimado** (500GB standard): ~$10/mes

#### AWS - S3
- **Costo**:
  - Standard: $0.023/GB/mes
  - Infrequent Access: $0.0125/GB/mes
  - Glacier: $0.004/GB/mes
- **Costo mensual estimado** (500GB standard): ~$12/mes

**Ganador**: GCP Cloud Storage (ligeramente más económico)

## Estimación de Costos Mensuales Totales

### Escenario: 1M tweets/día, procesamiento continuo

#### GCP
- Pub/Sub: ~$12/mes
- Dataflow: ~$80/mes
- Vertex AI Training: ~$50/mes
- Cloud Functions: ~$5/mes
- Cloud Storage: ~$10/mes
- **Total estimado: ~$157/mes**

#### AWS
- MSK: ~$144/mes (o $0 si se usa Kinesis)
- EMR (spot): ~$58/mes
- SageMaker: ~$50/mes
- Lambda: ~$3/mes
- S3: ~$12/mes
- **Total estimado: ~$267/mes** (con MSK)
- **Total estimado: ~$123/mes** (con Kinesis + EMR spot)

**Ahorro GCP**: ~$10-110/mes dependiendo de configuración

## Comparación de Rendimiento

### Latencia de Procesamiento
- **GCP Dataflow**: ~100-200ms por batch
- **AWS EMR**: ~150-300ms por batch (depende de configuración)

### Throughput
- **GCP Dataflow**: Hasta 100K mensajes/segundo (auto-scaling)
- **AWS EMR**: Hasta 200K mensajes/segundo (con configuración adecuada)

### Disponibilidad
- **GCP**: 99.95% SLA
- **AWS**: 99.99% SLA (con múltiples AZs)

### Escalabilidad
- **GCP Dataflow**: Auto-scaling automático
- **AWS EMR**: Auto-scaling manual/configurable

## Factores de Decisión

### Elegir GCP si:
- ✅ Ya usas otros servicios de GCP
- ✅ Prefieres simplicidad y auto-scaling
- ✅ Necesitas integración con BigQuery
- ✅ Presupuesto limitado
- ✅ Quieres menos gestión de infraestructura

### Elegir AWS si:
- ✅ Necesitas máximo control
- ✅ Requieres Kafka nativo (MSK)
- ✅ Quieres usar spot instances para ahorro
- ✅ Ya tienes infraestructura AWS
- ✅ Necesitas mayor throughput

## Optimización de Costos

### Estrategias Comunes:

1. **Usar instancias spot/preemptibles**: 60-90% ahorro
2. **Auto-scaling agresivo**: Reducir costos en horas de bajo uso
3. **Almacenamiento en frío**: Mover datos antiguos a cold storage
4. **Reserved Instances**: 30-40% descuento para cargas predecibles
5. **Monitoreo de costos**: Alertas y budgets

### Recomendaciones Específicas:

**Para GCP:**
- Usar preemptible VMs en Dataflow cuando sea posible
- Configurar lifecycle policies en Cloud Storage
- Usar Cloud Functions Gen 2 para mejor rendimiento/costo

**Para AWS:**
- Usar spot instances en EMR (hasta 90% ahorro)
- Considerar Kinesis en lugar de MSK si no necesitas Kafka nativo
- Usar S3 Intelligent-Tiering para almacenamiento

## Conclusión

Para este pipeline de análisis de sentimiento:

- **GCP es más económico** (~17% menos) para el escenario base
- **AWS ofrece más flexibilidad** y control, especialmente con spot instances
- **La diferencia es menor** con optimizaciones (spot instances, preemptibles)

**Recomendación final**: 
- **GCP** para simplicidad, costos predecibles y menos gestión
- **AWS** para control, Kafka nativo y optimización agresiva de costos con spot

## Próximos Pasos

1. Ejecutar pruebas de carga en ambos proveedores
2. Medir costos reales con cargas de trabajo reales
3. Implementar optimizaciones de costos
4. Documentar métricas de rendimiento reales
5. Configurar alertas de presupuesto

