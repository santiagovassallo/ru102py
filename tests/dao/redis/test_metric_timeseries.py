import datetime
from typing import Generator
from typing import List

import pytest

from redisolar.dao.redis import MetricDaoRedisTimeseries
from redisolar.models import MeterReading
from redisolar.models import MetricUnit

TESTING_SITE_ID = 1
NOW = datetime.datetime.utcnow()


@pytest.fixture
def metric_dao(redis_timeseries, key_schema):
    yield MetricDaoRedisTimeseries(redis_timeseries, key_schema)


@pytest.fixture
def readings(metric_dao) -> Generator[List[MeterReading], None, None]:
    """
    Generate 72 hours worth of data.

    Unlike with our sorted set implementation, RedisTimeSeries requires that we
    add entries in order. So we generate meter readings oldest to newest.

    We could also build a list and then reverse it, but where's the fun in
    that?
    """
    time = NOW - datetime.timedelta(hours=72)
    readings = []
    for i in range((72 * 60) - 1, -1, -1):
        readings.append(
            MeterReading(site_id=1,
                         temp_c=i * 1.0,
                         wh_used=i * 1.0,
                         wh_generated=i * 1.0,
                         timestamp=time))
        time = time + datetime.timedelta(minutes=1)
    yield readings


def _test_insert_and_retrieve(readings: List[MeterReading],
                              metric_dao: MetricDaoRedisTimeseries, limit: int):
    for reading in readings:
        metric_dao.insert(reading)

    measurements = metric_dao.get_recent(TESTING_SITE_ID, MetricUnit.WH_GENERATED, NOW,
                                         limit)
    assert len(measurements) == limit

    i = limit
    for measurement in measurements:
        assert measurement.value == (i - 1) * 1.0
        i -= 1


def test_small(metric_dao, readings):
    _test_insert_and_retrieve(readings, metric_dao, 1)


def test_one_day(metric_dao, readings):
    _test_insert_and_retrieve(readings, metric_dao, 60 * 24)


def test_multiple_days(metric_dao, readings):
    _test_insert_and_retrieve(readings, metric_dao, 60 * 70)