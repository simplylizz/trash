from pyspark.sql import SparkSession
from pyspark.sql import DataFrame
import pyspark.sql.types as T
from pyspark.sql import Window
import pyspark.sql.functions as F


_POSTGRES_CONNECT_URL = 'jdbc:postgresql://db:5432/postgres'
_POSTGRES_PROPERTIES = {'user': 'postgres'}


def _load_csv(spark: SparkSession, schema: T.StructType, file_name: str) -> DataFrame:
    return spark \
        .read \
        .format('csv') \
        .option('header', 'true')\
        .schema(schema) \
        .load(f'data/{file_name}')


def load_category_tree(spark: SparkSession) -> DataFrame:
    return _load_csv(
        spark=spark,
        schema=T.StructType([
            T.StructField('categoryid', T.IntegerType()),
            T.StructField('parentid', T.IntegerType()),
        ]),
        file_name='category_tree.csv',
    )


def load_events(spark: SparkSession) -> DataFrame:
    return _load_csv(
        spark=spark,
        schema=T.StructType([
            T.StructField('timestamp', T.LongType()),
            T.StructField('visitorid', T.IntegerType()),
            T.StructField('event', T.StringType()),
            T.StructField('itemid', T.IntegerType()),
            T.StructField('transactionid', T.IntegerType()),
        ]),
        file_name='events.csv',
    )


def load_category_tree(spark: SparkSession) -> DataFrame:
    return _load_csv(
        spark=spark,
        schema=T.StructType([
            T.StructField('categoryid', T.IntegerType()),
            T.StructField('parentid', T.IntegerType()),
        ]),
        file_name='category_tree.csv',
    )


def load_item_properties_part1(spark: SparkSession) -> DataFrame:
    return _load_csv(
        spark=spark,
        schema=T.StructType([
            T.StructField('timestamp', T.IntegerType()),
            T.StructField('itemid', T.IntegerType()),
            T.StructField('property', T.StringType()),
            T.StructField('value', T.StringType()),
        ]),
        file_name='item_properties_part1.csv',
    )


def load_item_properties_part2(spark: SparkSession) -> DataFrame:
    return _load_csv(
        spark=spark,
        schema=T.StructType([
            T.StructField('timestamp', T.IntegerType()),
            T.StructField('itemid', T.IntegerType()),
            T.StructField('property', T.StringType()),
            T.StructField('value', T.StringType()),
        ]),
        file_name='item_properties_part2.csv',
    )


def normalize_events(df: DataFrame) -> DataFrame:
    return df.withColumn(
        'timestamp',
        (df.timestamp / F.lit(1000)).cast('timestamp'),
    )


def main():
    spark = SparkSession.builder \
        .master('local[*]') \
        .config('spark.jars', '/opt/postgresql.jar') \
        .config('spark.driver.extraClassPath', '/opt/postgresql.jar') \
        .getOrCreate()

    # category_tree = load_category_tree(spark)
    # category_tree.show()

    events = load_events(spark)

    events = normalize_events(events)

    # calculate top 5 most viewed products per week

    events = events.withColumn(
        'week',
        F.weekofyear(F.col('timestamp')),
    )

    events = events.filter(F.col('event') == F.lit('view'))

    events = events.groupBy(F.col('itemid'), F.col('week')).agg(
        F.count(F.col('itemid')).alias('views'),
    )

    w = Window.partitionBy(
        F.col('week'),
    ).orderBy(
        F.col('views').desc(),
    )

    events = events.withColumn(
        'row',
        F.row_number().over(w),
    ).filter(
        F.col('row') <= F.lit(5),
    ).orderBy(
        F.col('week'),
        F.col('views').desc(),
    )

    events.show()

    # item_properties_part1 = load_item_properties_part1(spark)
    # item_properties_part1.show()

    # item_properties_part2 = load_item_properties_part2(spark)
    # item_properties_part2.show()

    # category_tree.write.jdbc(
    #     url=_POSTGRES_CONNECT_URL,
    #     table='category_tree',
    #     mode='overwrite',
    #     properties=_POSTGRES_PROPERTIES,
    # )


if __name__ == '__main__':
    main()
