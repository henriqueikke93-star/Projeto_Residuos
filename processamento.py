from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as _sum

# Inicializa a sessão do Spark dentro do Kubernetes
spark = SparkSession.builder \
    .appName("ProcessamentoResiduos") \
    .getOrCreate()

print("====== INICIANDO PROCESSAMENTO DOS DADOS ======")

# Lendo o CSV que está no volume compartilhado
df = spark.read.option("header", "true") \
               .option("sep", ";") \
               .option("inferSchema", "true") \
               .csv("/dados/residuos.csv")

# Selecionando e limpando as colunas reais do seu arquivo
df_limpo = df.select(
    col("Município Declarante").alias("municipio"),
    col("UF Declarante").alias("uf"),
    col("orr_descricao").alias("tipo_residuo"),
    col("Caracterização - Descrição").alias("categoria"),
    col("Massa (TON)").cast("double").alias("toneladas")
).na.fill(0, ["toneladas"])

# Agrupando por município e categoria para somar o peso total
df_agrupado = df_limpo.groupBy("municipio", "uf", "categoria") \
                      .agg(_sum("toneladas").alias("total_toneladas")) \
                      .filter(col("categoria").isNotNull())

# Salvando o resultado final consolidado de volta no volume
df_agrupado.coalesce(1) \
           .write \
           .mode("overwrite") \
           .option("header", "true") \
           .csv("/dados/resultado_processado")

print("====== PROCESSAMENTO CONCLUÍDO COM SUCESSO ======")
spark.stop()