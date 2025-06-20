from .AbstractCounter import StringCounter
from typing import Callable


class AdditiveCounter(StringCounter):
    def __init__(self, *counters: StringCounter):
        self.counters = counters
        super().__init__()

    def count(self, s: str) -> int:
        return sum(counter.count(s) for counter in self.counters)


class CompositeCounter(StringCounter):
    def __init__(
        self, counters: list[StringCounter], weights: list[float] | None = None
    ):
        self.counters = counters
        self.weights = weights if weights else [1] * len(counters)
        if len(self.counters) != len(self.weights):
            raise ValueError("Number of counters must match number of weights")
        super().__init__()

    def count(self, s: str) -> int:
        counts = [counter.count(s) for counter in self.counters]
        return int(sum(count * weight for count, weight in zip(counts, self.weights)))


class PipelineCounter(StringCounter):
    def __init__(self, *counters: StringCounter) -> None:
        self.counters = counters
        super().__init__()

    def count(self, s: str) -> int:
        result = s
        for counter in self.counters:
            result = str(counter.count(result))
        return int(result)


class ConditionalCounter(StringCounter):
    def __init__(
        self,
        condition: Callable,
        true_counter: StringCounter,
        false_counter: StringCounter,
    ):
        self.condition = condition
        self.true_counter = true_counter
        self.false_counter = false_counter
        super().__init__()

    def count(self, s: str) -> int:
        if self.condition(s):
            return self.true_counter.count(s)
        else:
            return self.false_counter.count(s)


class AggregateCounter(StringCounter):
    def __init__(self, counters: list[StringCounter], aggregator: Callable):
        self.counters = counters
        self.aggregator = aggregator
        super().__init__()

    def count(self, s: str) -> int:
        counts = [counter.count(s) for counter in self.counters]
        return self.aggregator(counts)


class ModifiedInputCounter(StringCounter):
    def __init__(self, base_counter: StringCounter, modifier: Callable):
        self.base_counter = base_counter
        self.modifier = modifier
        super().__init__()

    def count(self, s: str) -> int:
        modified_s = self.modifier(s)
        return self.base_counter.count(modified_s)


class CachedCounter(StringCounter):
    def __init__(self, base_counter: StringCounter):
        self.base_counter = base_counter
        self.cache = {}
        super().__init__()

    def count(self, s: str) -> int:
        if s not in self.cache:
            self.cache[s] = self.base_counter.count(s)
        return self.cache[s]


class ThresholdCounter(StringCounter):
    def __init__(self, base_counter: StringCounter, threshold: int):
        self.base_counter = base_counter
        self.threshold = threshold
        super().__init__()

    def count(self, s: str) -> int:
        count = self.base_counter.count(s)
        return 1 if count >= self.threshold else 0
