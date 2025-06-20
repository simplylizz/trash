# flake8: noqa: E731

import unittest
import random
from project.ComposedCounters import (
    AdditiveCounter,
    CompositeCounter,
    PipelineCounter,
    ConditionalCounter,
    AggregateCounter,
    ModifiedInputCounter,
    CachedCounter,
    ThresholdCounter,
)
from .helpers import _test_composed_counter_serialization


class TestComposedCounterSerialization(unittest.TestCase):
    def test_additive_counter_serialization(self):
        gen_additive_counter = lambda counters: AdditiveCounter(*counters)
        _test_composed_counter_serialization(self, gen_additive_counter)

    def test_composite_counter_serialization(self):
        weight_gen = lambda counters: [random.random() for _ in range(len(counters))]
        gen_composite_counter = lambda counters: CompositeCounter(
            counters, weight_gen(counters)
        )
        _test_composed_counter_serialization(self, gen_composite_counter)

    def test_pipeline_counter_serialization(self):
        gen_pipeline_counter = lambda counters: PipelineCounter(*counters)
        _test_composed_counter_serialization(self, gen_pipeline_counter)

    def test_conditional_counter_serialization(self):
        conditions = [
            lambda s: len(s) > 5,
            lambda s: s.isupper(),
            lambda s: s.isdigit(),
        ]
        gen_conditional_counter = lambda counters: ConditionalCounter(
            random.choice(conditions), counters[0], counters[1]
        )
        _test_composed_counter_serialization(
            self, gen_conditional_counter, num_basic_counters=2
        )

    def test_aggregate_counter_serialization(self):
        aggregators = [max, min, sum, lambda counts: sum(counts) / len(counts)]
        gen_aggregate_counter = lambda counters: AggregateCounter(
            counters, random.choice(aggregators)
        )
        _test_composed_counter_serialization(self, gen_aggregate_counter)

    def test_modified_input_counter_serialization(self):
        modifiers = [
            lambda s: s.upper(),
            lambda s: s.lower(),
            lambda s: str(s)[::-1],
            lambda s: s.replace("a", "b"),
        ]
        gen_modified_input_counter = lambda counters: ModifiedInputCounter(
            counters[0], random.choice(modifiers)
        )
        _test_composed_counter_serialization(
            self, gen_modified_input_counter, num_basic_counters=1
        )

    def test_cached_counter_serialization(self):
        gen_cached_counter = lambda counters: CachedCounter(counters[0])
        _test_composed_counter_serialization(
            self, gen_cached_counter, num_basic_counters=1
        )

    def test_threshold_counter_serialization(self):
        gen_threshold_counter = lambda counters: ThresholdCounter(
            counters[0], random.randint(1, 1000)
        )
        _test_composed_counter_serialization(
            self, gen_threshold_counter, num_basic_counters=1
        )


if __name__ == "__main__":
    unittest.main()
