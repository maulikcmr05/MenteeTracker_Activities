LOAD CSV WITH HEADERS FROM 'file:///orders.csv' AS r
MERGE (c:Customer {id:r.customer_id})
MERGE (p:Product {name:r.product})
MERGE (o:Order {id:toInteger(r.order_id)})
SET o.region=r.region,o.quantity=toInteger(r.quantity),o.unit_price=toFloat(r.unit_price)
MERGE (c)-[:PLACED]->(o)
MERGE (o)-[:CONTAINS]->(p);
MATCH (c:Customer)-[:PLACED]->(o)-[:CONTAINS]->(p)
RETURN c.id,p.name,sum(o.quantity) AS units;
