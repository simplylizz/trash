from BasicCounters import LengthCounter, VowelCounter
from ComposedCounters import AdditiveCounter

# Create a Composed Counter
additive_counter = AdditiveCounter(LengthCounter(), VowelCounter())

# Use the counter
original_count = additive_counter.count("Hello, World!")
print(f"Original count: {original_count}")

# Serialize the counter
serialized_data = additive_counter.serialize()

# Deserialize the counter
deserialized_counter = VowelCounter.deserialize(serialized_data)

# Use the deserialized counter
deserialized_count = deserialized_counter.count("Hello, World!")
print(f"Deserialized count: {deserialized_count}")

assert original_count == deserialized_count
print("Serialization and deserialization of Composed Counter successful!")