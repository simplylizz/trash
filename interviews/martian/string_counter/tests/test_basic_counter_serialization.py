import unittest
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
from .helpers import _test_counter_serialization


class TestBasicCounterSerialization(unittest.TestCase):
    def test_length_counter_serialization(self):
        _test_counter_serialization(self, LengthCounter())

    def test_vowel_counter_serialization(self):
        _test_counter_serialization(self, VowelCounter())

    def test_byte_counter_serialization(self):
        _test_counter_serialization(self, ByteCounter())

    def test_word_counter_serialization(self):
        _test_counter_serialization(self, WordCounter())

    def test_char_occurrence_counter_serialization(self):
        for char in ["a", "Z", "1", "@", " ", ".", "!", "9"]:
            _test_counter_serialization(self, CharOccurrenceCounter(char))

    def test_randomized_counter_serialization(self):
        for seed in [42, 0, 1337, 100, 999]:
            _test_counter_serialization(self, RandomizedCounter(seed=seed))

    def test_hash_based_counter_serialization(self):
        _test_counter_serialization(self, HashBasedCounter())

    def test_stateful_counter_serialization(self):
        _test_counter_serialization(self, StatefulCounter())


if __name__ == "__main__":
    unittest.main()
