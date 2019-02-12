FROM neo4j:3.2

ENV NEO4J_PASSWD neo4jadmin
ENV NEO4J_AUTH neo4j/${NEO4J_PASSWD}

COPY ./beverages.cypher /tmp/data.cypher

CMD bin/neo4j-admin set-initial-password ${NEO4J_PASSWD} || true && \
    bin/neo4j start && sleep 5 && \
    cat /tmp/data.cypher | /var/lib/neo4j/bin/cypher-shell -u neo4j -p ${NEO4J_PASSWD} && \
    tail -f logs/neo4j.log