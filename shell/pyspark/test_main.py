import datetime

import pytest

from pyspark.sql import SparkSession
import pyspark.sql.types as T

import main


@pytest.fixture
def spark():
    return SparkSession.builder \
        .master('local[*]') \
        .config('spark.jars', '/opt/postgresql.jar') \
        .config('spark.driver.extraClassPath', '/opt/postgresql.jar') \
        .getOrCreate()


def test_normalize_events(spark: SparkSession):
    df = spark.createDataFrame(
        [
            # ts is in ms in the original data
            (0, ),
            (1000, ),
            (-1000, ),
        ],
        schema=T.StructType([T.StructField('timestamp', T.LongType())]),
    )

    df = main.normalize_events(df)

    expected_df = spark.createDataFrame(
        [
            (datetime.datetime(1970, 1, 1, 0, 0, 0), ),
            (datetime.datetime(1970, 1, 1, 0, 0, 1), ),
            (datetime.datetime(1969, 12, 31, 23, 59, 59), ),
        ],
        schema=T.StructType([T.StructField('timestamp', T.TimestampType())]),
    )

    assert df.collect() == expected_df.collect()
