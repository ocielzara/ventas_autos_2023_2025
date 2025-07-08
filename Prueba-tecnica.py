# -------------------------------------
# Análisis de ventas de autos 2023–2025
# -------------------------------------

import pandas as pd

# ===============================
# 1. CARGA Y LIMPIEZA DE DATOS
# ===============================

# Cargar dataset desde GitHub
ruta_archivo = 'https://raw.githubusercontent.com/gerenciabigh/test_datasets/refs/heads/main/ventas_autos_2023_2025.csv'
df = pd.read_csv(ruta_archivo)

# Verificación inicial
print(df.head())
print(df.info())
print(df.isnull().sum())  # Ventas tiene 71% valores faltantes

# Rellenar valores nulos en ventas con cero
df['ventas'] = df['ventas'].fillna(0)

# ===============================
# 2. ANÁLISIS DE VENTAS POR CATEGORÍA
# ===============================

# Total de ventas por marca
ventas_por_marca = df.groupby('marca')['ventas'].sum().sort_values(ascending=False)
print("Ventas totales por marca:\n", ventas_por_marca)

# Hallazgos clave:
# - Nissan lidera con más de 600 mil unidades.
# - Le siguen General Motors y Volkswagen.
# - Marcas emergentes como MG Motor y Chirey están creciendo fuerte.

# Total de ventas por tipo de vehículo
ventas_por_tipo = df.groupby('tipo')['ventas'].sum().sort_values(ascending=False)
print("\nVentas totales por tipo de vehículo:\n", ventas_por_tipo)

# Relevante:
# - Los camiones ligeros superan a los automóviles, representando el 57% del total.

# Total por origen (nacional vs importado)
ventas_por_origen = df.groupby('origen')['ventas'].sum()
print("\nVentas totales por origen:\n", ventas_por_origen)

# Insights:
# - 66% de los vehículos vendidos son importados alta dependencia del extranjero.

# ===============================
# 3. PROCESAMIENTO TEMPORAL
# ===============================

# Convertir mes textual a número
meses = {
    'Enero': 1, 'Febrero': 2, 'Marzo': 3, 'Abril': 4,
    'Mayo': 5, 'Junio': 6, 'Julio': 7, 'Agosto': 8,
    'Septiembre': 9, 'Octubre': 10, 'Noviembre': 11, 'Diciembre': 12
}
df['mes_num'] = df['mes'].map(meses)

# Crear columna tipo fecha
df['fecha'] = pd.to_datetime(
    df[['año', 'mes_num']].rename(columns={'año': 'year', 'mes_num': 'month'}).assign(day=1)
)

# ===============================
# 4. PARTICIPACIÓN DE MERCADO MENSUAL
# ===============================

marca_mes = df.groupby(['fecha', 'marca'])['ventas'].sum().reset_index()
marca_mes['total_ventas_mes'] = marca_mes.groupby('fecha')['ventas'].transform('sum')
marca_mes['participacion_marca'] = marca_mes['ventas'] / marca_mes['total_ventas_mes']
print("\n Participación mensual de las marcas:\n", marca_mes.head(115))

# Valor estratégico:
# - KIA y Mazda muestran crecimiento sostenido de participación mensual.
# - Algunas marcas grandes pierden tracción en ciertos meses (por ejemplo GM en marzo 2023 con 0 ventas).

# ===============================
# 5. VENTAS POR PAÍS DE ORIGEN
# ===============================

ventas_pais = df.groupby('pais_origen')['ventas'].sum().sort_values(ascending=False)
print("\nVentas totales por país de origen:\n", ventas_pais)

ventas_pais_pct = ventas_pais / ventas_pais.sum() * 100
print("\nParticipación porcentual por país de origen:\n", ventas_pais_pct)

# Hallazgos:
# - México lidera (34%), seguido por China (20%) y Brasil/EEUU (8%).
# - China muestra una presencia agresiva → debe observarse para prever anomalias en el mercado.

# ===============================
# 6. MODELOS CON VENTAS NULAS
# ===============================

# Modelos con más de 12 meses sin ventas
modelos_sin_ventas = df[df['ventas'] == 0].groupby(['marca', 'modelo']).size().sort_values(ascending=False)
apariciones_totales = df.groupby(['marca', 'modelo']).size()
proporcion_nula = (modelos_sin_ventas / apariciones_totales).sort_values(ascending=False)
modelos_frecuentes_sin_ventas = modelos_sin_ventas[modelos_sin_ventas > 12]

print("\nModelos con ventas nulas en más de 12 periodos:\n", modelos_frecuentes_sin_ventas.head(20))
print("\nProporción de registros sin ventas por modelo:\n", proporcion_nula.head(20))

# Relevancia para gestión:
# - Algunos modelos como Yaris Hatchback, Silverado 2500, T-Cross y Fiesta Sedan figuran en el catálogo sin ventas por más de un año.
# - Ineficiencias que podría generar costos logísticos o de inventario innecesarios.
# - Recomendación: revisar portafolio de productos activos y ajustar mix de modelos.

# ===============================
# 7. CONCLUSIONES
# ===============================

# Principales hallazgos:
# - Nissan, GM y VW lideran, pero marcas como KIA y MG Motor están ganando cuota.
# - Camiones ligeros dominan la preferencia del consumidor.
# - Importación masiva (66%) sugiere vulnerabilidad ante cambios bruscos logísticos.
# - China ya es el segundo mayor origen de vehículos.
# - Existen al menos 100 modelos con ventas nulas por más de 12 meses oportunidad clara de optimización de portafolio.

# Principales insights:
# - Nissan lidera el mercado mexicano con más de 600 mil unidades vendidas, seguido por General Motors y Volkswagen.
# - Marcas emergentes como MG Motor y Chirey muestran un crecimiento acelerado, ganando participación rápidamente, lo que indica un cambio en la preferencia del consumidor hacia opciones más accesibles o tecnológicamente atractivas.
# - Los camiones ligeros representan el 57% del total de ventas, superando a los automóviles. Esto sugiere: Una preferencia por vehículos utilitarios y de carga.
# - 66% de los vehículos vendidos son importados, lo que: Representa una fuerte dependencia del comercio exterior.
# - China es el segundo mayor país de origen, con el 20% del total, solo detrás de México (34%): China está desplazando a potencias tradicionales como EE.UU., Japón y Alemania. Esto confirma una tendencia de penetración asiática en Latinoamérica, tanto en marcas nuevas como en modelos económicos.
# - Se detectaron más de 100 modelos con 12 o más meses consecutivos sin ventas: Ejemplos críticos: Toyota Yaris Hatchback, Silverado 2500, Fiesta Sedan, Peugeot 308. Esto indica una ineficiencia comercial y operativa, con posibles costos innecesarios de inventario o marketing.
