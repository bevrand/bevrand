FROM neo4j:3.2

ENV NEO4J_PASSWD neo4jadmin
ENV NEO4J_AUTH neo4j/${NEO4J_PASSWD}

COPY data.cypher /var/lib/neo4j/import/

VOLUME /data

CMD bin/neo4j-admin set-initial-password ${NEO4J_PASSWD} || true && \
    bin/neo4j start && sleep 5 && \
    for f in import/*; do \
      [ -f "$f" ] || continue; \
      cat "$f" | NEO4J_USERNAME=neo4j NEO4J_PASSWORD=${NEO4J_PASSWD} bin/cypher-shell --fail-fast && rm "$f"; \
    done && \
    tail -f logs/neo4j.log