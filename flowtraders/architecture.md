# Initial conditions

We have many internal systems generating events at a peak rate of ~100k events/s (e.g market 
data updates, prices and trades). These events are highly structured and include identifiers 
that relate to events and metadata in other systems. The source systems do not support 
back-pressure, any dropped messages are lost.

Design a system that is able to process and enrich these events with information from other systems,
and then display a dynamic selection of the information to multiple users in real-time with updates. 
We expect a system level design describing the major components and reasons for using them. 
Limit the detail to a single page.

# Design

High-level architecture.

## Collector
A bunch of frontend service behind load balancer which accepts messages,
makes very basic validation and puts them to message bus (auth could be plugged in here
if required, or if we are working with internal system in trustworthy environment, we can
omit such service at all and push messages directly to the message bus).

So message bus is kind of buffer which should be able to accumulate large volume of data.
I'd stick with PubSub if there is no any restrictions since I've worked with it more,
also it's managed solution, so should allow to start fast without any deep performance tuning.
Another alternatives to consider: NSQ, Kafka or RabbitMQ.

## Enricher
If we want to stick with managed solutions I'd prefer to use Apache Beam / Dataflow.
It could handle workload pretty good, also provides some metrics out of the box like
data freshness / lag.

Pros:
- Autoscaling out of the box.
- It provides some metrics like data lag / data freshness.
- It's quite flexible.
- Supports a lot of sink and source formats.
- Managed solution (should 'just work').

Cons:
- Because of flexibility it has sometimes too much options to consider.
- Nevertheless sometimes it doesn't provide enough options (e.g. you can't
  specify on your own 'insertion id' for BigQuery which allows to prevent
  duplicate records).
- If something goes wrong debugging could be quite tricky.
- Managed solution (it out of your control and you need to think about cost).

So as alternative it could be a bunch of microservices with separate autoscaler service which
could monitor processing speed, size of backlog (i.e. unprocessed messages) and decide
if we need to add more enrichers.

Enriched data could be published back into message bus for further processing.

## Loader
One more Apache Beam pipeline or custom microservice which pulls data from PubSub and
tries to write it to target database (e.g. BigQuery, Clickhouse or ElasticSearch, MongoDB).

Collector, enricher and loader could write faulty messages to special sinks for
the observability's sake.

## Serialization format
Another important thing to consider is a message serialization format.
I've never worked with MessagePack, but according to some benchmarks it's super compact
and quite performant, also outperforms Protobuf (by all means, again, according to some™
benchmarks on the Internet). So I'd consider it as candidate #1.

Though Protobuf, Flatbuffers and some other alternatives could be considered as well.
