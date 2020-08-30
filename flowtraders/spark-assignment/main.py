from pyspark.sql import SparkSession
from pyspark.sql import DataFrame
import pyspark.sql.types as T
from pyspark.sql import Window
import pyspark.sql.functions as F


def load_trades(spark):
    data = [
        (10, 1546300800000, 37.50, 100.000),
        (10, 1546300801000, 37.51, 100.000),
        (20, 1546300804000, 12.67, 300.000),
        (10, 1546300807000, 37.50, 200.000),
    ]
    schema = T.StructType(
        [
            T.StructField("id", T.LongType()),
            T.StructField("timestamp", T.LongType()),
            # just for the record: usually double isn't the best choice for price and quantity
            # decimal or multiplied ints (aka scaled/fixed-point arithmetic) may fit better
            T.StructField("price", T.DoubleType()),
            T.StructField("quantity", T.DoubleType()),
        ]
    )

    return spark.createDataFrame(data, schema)


def load_prices(spark):
    data = [
        (10, 1546300799000, 37.50, 37.51),
        (10, 1546300802000, 37.51, 37.52),
        (10, 1546300806000, 37.50, 37.51),
    ]
    schema = T.StructType(
        [
            T.StructField("id", T.LongType()),
            T.StructField("timestamp", T.LongType()),
            T.StructField("bid", T.DoubleType()),
            T.StructField("ask", T.DoubleType()),
        ]
    )

    return spark.createDataFrame(data, schema)


def union_trades_and_prices(trades: DataFrame, prices: DataFrame) -> DataFrame:
    return prices.withColumn(
        'price',
        F.lit(None).cast('double'),
    ).withColumn(
        'quantity',
        F.lit(None).cast('double'),
    ).unionByName(
        trades.withColumn(
            'ask',
            F.lit(None).cast('double'),
        ).withColumn(
            'bid',
            F.lit(None).cast('double'),
        ),
    )


def fill(trades, prices):
    """
    Combine the sets of events and fill forward the value columns so that each
    row has the most recent non-null value for the corresponding id. For
    example, given the above input tables the expected output is:

    +---+-------------+-----+-----+-----+--------+
    | id|    timestamp|  bid|  ask|price|quantity|
    +---+-------------+-----+-----+-----+--------+
    | 10|1546300799000| 37.5|37.51| null|    null|
    | 10|1546300800000| 37.5|37.51| 37.5|   100.0|
    | 10|1546300801000| 37.5|37.51|37.51|   100.0|
    | 10|1546300802000|37.51|37.52|37.51|   100.0|
    | 20|1546300804000| null| null|12.67|   300.0|
    | 10|1546300806000| 37.5|37.51|37.51|   100.0|
    | 10|1546300807000| 37.5|37.51| 37.5|   200.0|
    +---+-------------+-----+-----+-----+--------+

    :param trades: DataFrame of trade events
    :param prices: DataFrame of price events
    :return: A DataFrame of the combined events and filled.

    >>> spark = SparkSession.builder.master("local[*]").getOrCreate()
    >>> trades = load_trades(spark)
    >>> prices = load_prices(spark)
    >>> fill(trades=trades, prices=prices).orderBy('timestamp').show()
    +---+-------------+-----+-----+-----+--------+
    | id|    timestamp|  bid|  ask|price|quantity|
    +---+-------------+-----+-----+-----+--------+
    | 10|1546300799000| 37.5|37.51| null|    null|
    | 10|1546300800000| 37.5|37.51| 37.5|   100.0|
    | 10|1546300801000| 37.5|37.51|37.51|   100.0|
    | 10|1546300802000|37.51|37.52|37.51|   100.0|
    | 20|1546300804000| null| null|12.67|   300.0|
    | 10|1546300806000| 37.5|37.51|37.51|   100.0|
    | 10|1546300807000| 37.5|37.51| 37.5|   200.0|
    +---+-------------+-----+-----+-----+--------+
    ...
    """

    union_df = union_trades_and_prices(trades, prices)

    w = Window.partitionBy("id").orderBy("timestamp")

    for col_name in ('ask', 'bid', 'price', 'quantity'):
        union_df = union_df.withColumn(
            col_name,
            F.last(
                F.col(col_name),
                ignorenulls=True,
            ).over(w),
        )

    return union_df


def pivot(trades, prices):
    """
    Pivot and fill the columns on the event id so that each row contains a
    column for each id + column combination where the value is the most recent
    non-null value for that id. For example, given the above input tables the
    expected output is:

    +---+-------------+-----+-----+-----+--------+------+------+--------+-----------+------+------+--------+-----------+
    | id|    timestamp|  bid|  ask|price|quantity|10_bid|10_ask|10_price|10_quantity|20_bid|20_ask|20_price|20_quantity|
    +---+-------------+-----+-----+-----+--------+------+------+--------+-----------+------+------+--------+-----------+
    | 10|1546300799000| 37.5|37.51| null|    null|  37.5| 37.51|    null|       null|  null|  null|    null|       null|
    | 10|1546300800000| null| null| 37.5|   100.0|  37.5| 37.51|    37.5|      100.0|  null|  null|    null|       null|
    | 10|1546300801000| null| null|37.51|   100.0|  37.5| 37.51|   37.51|      100.0|  null|  null|    null|       null|
    | 10|1546300802000|37.51|37.52| null|    null| 37.51| 37.52|   37.51|      100.0|  null|  null|    null|       null|
    | 20|1546300804000| null| null|12.67|   300.0| 37.51| 37.52|   37.51|      100.0|  null|  null|   12.67|      300.0|
    | 10|1546300806000| 37.5|37.51| null|    null|  37.5| 37.51|   37.51|      100.0|  null|  null|   12.67|      300.0|
    | 10|1546300807000| null| null| 37.5|   200.0|  37.5| 37.51|    37.5|      200.0|  null|  null|   12.67|      300.0|
    +---+-------------+-----+-----+-----+--------+------+------+--------+-----------+------+------+--------+-----------+

    :param trades: DataFrame of trade events
    :param prices: DataFrame of price events
    :return: A DataFrame of the combined events and pivoted columns.

    >>> spark = SparkSession.builder.master("local[*]").getOrCreate()
    >>> trades = load_trades(spark)
    >>> prices = load_prices(spark)
    >>> pivot(trades=trades, prices=prices).orderBy('timestamp').show()
    +---+-------------+-----+-----+-----+--------+------+------+--------+-----------+------+------+--------+-----------+
    | id|    timestamp|  bid|  ask|price|quantity|10_bid|10_ask|10_price|10_quantity|20_bid|20_ask|20_price|20_quantity|
    +---+-------------+-----+-----+-----+--------+------+------+--------+-----------+------+------+--------+-----------+
    | 10|1546300799000| 37.5|37.51| null|    null|  37.5| 37.51|    null|       null|  null|  null|    null|       null|
    | 10|1546300800000| null| null| 37.5|   100.0|  37.5| 37.51|    37.5|      100.0|  null|  null|    null|       null|
    | 10|1546300801000| null| null|37.51|   100.0|  37.5| 37.51|   37.51|      100.0|  null|  null|    null|       null|
    | 10|1546300802000|37.51|37.52| null|    null| 37.51| 37.52|   37.51|      100.0|  null|  null|    null|       null|
    | 20|1546300804000| null| null|12.67|   300.0| 37.51| 37.52|   37.51|      100.0|  null|  null|   12.67|      300.0|
    | 10|1546300806000| 37.5|37.51| null|    null|  37.5| 37.51|   37.51|      100.0|  null|  null|   12.67|      300.0|
    | 10|1546300807000| null| null| 37.5|   200.0|  37.5| 37.51|    37.5|      200.0|  null|  null|   12.67|      300.0|
    +---+-------------+-----+-----+-----+--------+------+------+--------+-----------+------+------+--------+-----------+
    ...
    """

    # Disclaimer: in general, I don't like this solution by two main
    # reasons:
    # 1. Fetching unique ids without any prior knowledge about data
    #    doesn't feels like the right way. Though I assume that
    #    cardinality isn't super high, but if it is, then adding for
    #    each unique id 4 extra columns doesn't sounds great anyway.
    # 2. Also usage of window without partitioning is quite
    #    questionable approach.

    union_df = union_trades_and_prices(trades, prices)

    unique_ids_df = union_df.select(F.col('id')).distinct()
    unique_ids = [row.id for row in unique_ids_df.collect()]

    w = Window.orderBy('timestamp')

    fields = ('bid', 'ask', 'price', 'quantity')

    for unique_id in unique_ids:
        for f_name in fields:
            union_df = union_df.withColumn(
                f'{unique_id}_{f_name}',
                F.when(
                    union_df.id == F.lit(unique_id),
                    F.col(f_name),
                ),
            ).withColumn(
                f'{unique_id}_{f_name}',
                F.last(
                    F.col(f'{unique_id}_{f_name}'),
                    ignorenulls=True,
                ).over(w),
            )

    return union_df


def main():
    spark = SparkSession.builder.master("local[*]").getOrCreate()

    trades = load_trades(spark)
    trades.show()

    prices = load_prices(spark)
    prices.show()

    fill(trades, prices).orderBy('timestamp').show()

    pivot(trades, prices).orderBy('timestamp').show()


if __name__ == "__main__":
    main()
