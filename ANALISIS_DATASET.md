# Análisis del Dataset Sentiment140

## Información General

**Dataset:** Sentiment140  
**Fuente:** Kaggle (https://www.kaggle.com/datasets/kazanova/sentiment140)  
**Tipo:** Análisis de Sentimiento  
**Tamaño:** ~1.6 millones de tweets

## Estructura del Dataset

### Archivos

1. **train_data.csv** (~98 MB)

   - Dataset de entrenamiento
   - 1,523,976 registros (incluyendo header)
   - ~1,523,975 registros de datos
   - Columnas: `sentence`, `sentiment`

2. **test_data.csv** (~26 KB)

   - Dataset de prueba
   - 360 registros (incluyendo header)
   - ~359 registros de datos
   - Columnas: `sentence`, `sentiment`

3. **vocab.json** (~1.1 MB)

   - Vocabulario preprocesado
   - Diccionario de palabras

4. **vocab.py**

   - Script para procesar vocabulario

5. **Exploring Data.ipynb**
   - Notebook de exploración de datos

## Formato de Datos

### Columnas

- **sentence**: Texto del tweet (string)
- **sentiment**: Etiqueta de sentimiento
  - `0`: Negativo
  - `1`: Positivo

### Ejemplo de Datos

```csv
sentence,sentiment
"i loooooooovvvvvveee my kindle not that the dx is cool but the is fantastic in its own right",1
"reading my kindle love it lee childs is good read",1
"awww that s a bummer you shoulda got david carr of third day to do it d",0
"is upset that he can t update his facebook by texting it and might cry as a result school today also blah",0
```

## Estadísticas

### Train Data

- **Total de registros:** 1,523,976 (incluyendo header)
- **Registros de datos:** ~1,523,975
- **Tamaño del archivo:** ~98 MB
- **Distribución:** Balanceada entre positivo (1) y negativo (0)
- **Formato:** CSV con columnas `sentence` y `sentiment`

### Test Data

- **Total de registros:** 360 (incluyendo header)
- **Registros de datos:** ~359
- **Uso:** Validación del modelo
- **Formato:** CSV con columnas `sentence` y `sentiment`

## Características

- ✅ Datos preprocesados
- ✅ Vocabulario incluido
- ✅ Balanceado (positivo/negativo)
- ✅ Formato CSV estándar
- ✅ Listo para entrenamiento

## Uso en el Proyecto

Este dataset se utilizará para:

1. **Entrenamiento del modelo** de clasificación de sentimiento
2. **Validación** del pipeline de ML
3. **Pruebas** de procesamiento distribuido con Spark
4. **Benchmarking** de rendimiento

## Preprocesamiento

El dataset ya incluye:

- Vocabulario procesado (`vocab.json`)
- Scripts de procesamiento (`vocab.py`)
- Notebook de exploración

## Notas

- Los datos son tweets reales de Twitter
- Contienen lenguaje informal y abreviaciones
- Requieren limpieza adicional para producción
- El vocabulario puede necesitar actualización

## Ubicación

Los archivos del dataset se encuentran en:

```
data/raw/
├── train_data.csv
├── test_data.csv
├── vocab.json
├── vocab.py
└── Exploring Data.ipynb
```
