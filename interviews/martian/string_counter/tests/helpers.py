import random
import string
from typing import Callable, List
from project.AbstractCounter import StringCounter
from project.BasicCounters import (
    LengthCounter,
    VowelCounter,
    ByteCounter,
    WordCounter,
    CharOccurrenceCounter,
    RandomizedCounter,
    HashBasedCounter,
    StatefulCounter,

)



def get_random_basic_counters(n: int | None = None) -> list[StringCounter]:
    basic_counter_classes = [
        LengthCounter,
        VowelCounter,
        ByteCounter,
        WordCounter,
        CharOccurrenceCounter,
        RandomizedCounter,
        HashBasedCounter,
        StatefulCounter,
    ]

    if n is None:
        n = random.randint(1, 15)
    counters = []
    for _ in range(n):
        counter_class = random.choice(basic_counter_classes)
        if counter_class == CharOccurrenceCounter:
            counter = counter_class(random.choice(string.ascii_letters))
        elif counter_class == RandomizedCounter:
            counter = counter_class(seed=random.randint(0, 1000))
        elif counter_class == ByteCounter:
            counter = counter_class(
                encoding=random.choice(["utf-8", "ascii", "utf-16"])
            )
        else:
            counter = counter_class()
        counters.append(counter)

    return counters


def _test_counter_serialization(test_case, counter, num_tests=30, max_string_length=50):
    for _ in range(num_tests):
        # Generate a random string
        test_string = "".join(
            random.choices(
                string.ascii_letters + string.digits + string.punctuation + " ",
                k=random.randint(1, max_string_length),
            )
        )

        # Test the counter's first execution
        serialized_data = counter.serialize()
        deserialized_counter = StringCounter.deserialize(serialized_data)

        test_case.assertEqual(type(counter), type(deserialized_counter))
        test_case.assertEqual(
            counter.count(test_string), deserialized_counter.count(test_string)
        )
        # Test a second execution to check for statefulness
        serialized_data_2 = counter.serialize()
        # breakpoint()
        deserialized_counter_2 = StringCounter.deserialize(serialized_data_2)
        test_case.assertEqual(
            counter.count(test_string), deserialized_counter_2.count(test_string)
        )


def _test_composed_counter_serialization(
    test_case,
    gen_composed_counter: Callable[[List[StringCounter]], StringCounter],
    num_param_sets=20,
    num_basic_counters=None,
):
    for _ in range(num_param_sets):
        basic_counters = get_random_basic_counters(num_basic_counters)
        counter = gen_composed_counter(basic_counters)
        _test_counter_serialization(test_case, counter)
