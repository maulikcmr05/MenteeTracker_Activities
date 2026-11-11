import os
from cassandra.cluster import Cluster
c=Cluster([os.getenv("CASSANDRA_HOST","127.0.0.1")]); s=c.connect()
s.execute("CREATE KEYSPACE IF NOT EXISTS analytics WITH replication={'class':'SimpleStrategy','replication_factor':1}")
s.set_keyspace("analytics"); s.execute("CREATE TABLE IF NOT EXISTS counts(kind text PRIMARY KEY,n bigint)")
for k,n in [("click",7),("purchase",6),("view",7)]: s.execute("INSERT INTO counts(kind,n) VALUES(%s,%s)",(k,n))
c.shutdown()
