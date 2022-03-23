from clickhouse_driver import Client

subs = [
    ("10.102.3.11", "9001"),
    ("10.102.3.11", "9002"),
    ("10.102.3.11", "9003"),
    ("10.102.3.12", "9001"),
    ("10.102.3.12", "9002"),
    ("10.102.3.12", "9003"),
    ("10.102.3.13", "9001"),
    ("10.102.3.13", "9002"),
    ("10.102.3.13", "9003")
]

for sub in subs:
    client = Client(sub[0], port=sub[1])

    client.execute("CREATE DATABASE IF NOT EXISTS example")

    client.execute(r'''CREATE TABLE IF NOT EXISTS example.measures(
                      timestamp DateTime,
                      parameter String,
                      value Float64)
                      ENGINE = ReplicatedMergeTree('/clickhouse/tables/{shard}/example.measures', '{replica}')
                      PARTITION BY parameter
                      ORDER BY timestamp''')

for sub in subs:
    client = Client(sub[0], port=sub[1])

    client.execute('''CREATE TABLE IF NOT EXISTS example.measures_distr(
                      timestamp DateTime,
                      parameter String,
                      value Float64)
                      ENGINE = Distributed(clickhouse_cluster, example, measures, rand())''')
