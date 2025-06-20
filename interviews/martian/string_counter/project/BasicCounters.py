import random
from .AbstractCounter import StringCounter


class LengthCounter(StringCounter):
    def count(self, s: str) -> int:
        return len(s)


class VowelCounter(StringCounter):
    def count(self, s: str) -> int:
        return sum(1 for char in s.lower() if char in "aeiou")


class ByteCounter(StringCounter):
    def __init__(self, encoding="utf-8"):
        self.encoding = encoding
        super().__init__()

    def count(self, s: str) -> int:
        return len(s.encode(self.encoding))


class WordCounter(StringCounter):
    def count(self, s: str) -> int:
        return len(s.split())


class CharOccurrenceCounter(StringCounter):
    def __init__(self, char: str):
        self.char = char.lower()
        super().__init__()

    def count(self, s: str) -> int:
        return s.lower().count(self.char)


class RandomizedCounter(StringCounter):
    def __init__(self, seed: int = 42):
        self.rng = random.Random(seed)
        self.seed = seed
        super().__init__()

    def count(self, s: str) -> int:
        return self.rng.randint(0, len(s))


class HashBasedCounter(StringCounter):
    def __init__(self, modulus: int = 1000000007):
        self.modulus = modulus
        super().__init__()

    def count(self, s: str) -> int:
        hash_value = 0
        for char in s:
            hash_value = (hash_value * 31 + ord(char)) % self.modulus
        return hash_value


class StatefulCounter(StringCounter):
    def __init__(self):
        self.state = 0
        super().__init__()

    def count(self, s: str) -> int:
        self.state += 1
        return self.state
