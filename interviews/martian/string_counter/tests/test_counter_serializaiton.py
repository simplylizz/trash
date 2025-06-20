from project.BasicCounters import ByteCounter, CharOccurrenceCounter

# Create an instance of ByteCounter
byte_counter = ByteCounter(encoding='utf-16')

# Serialize the object to a human-readable string
serialized_str = byte_counter.serialize()
print("Serialized ByteCounter:")
print(serialized_str)

byte_counter_2 = ByteCounter.deserialize(serialized_str)



print(byte_counter)
print(byte_counter_2)

##


# Create an instance of ByteCounter
byte_counter = CharOccurrenceCounter(char='test tes')

# Serialize the object to a human-readable string
serialized_str = byte_counter.serialize()
print("Serialized ByteCounter:")
print(serialized_str)

byte_counter_2 = CharOccurrenceCounter.deserialize(serialized_str)


print(byte_counter)
print(byte_counter_2)