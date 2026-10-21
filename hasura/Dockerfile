# GraphQL API of the explorer: Hasura with the metadata from this directory.
# The schema itself is owned by pouw-indexer (Alembic), Hasura only tracks it.
#
# On start the image applies metadata/ and refuses to start if it references
# tables or columns that do not exist (inconsistent metadata).
FROM hasura/graphql-engine:v2.51.1.cli-migrations-v3

ENV HASURA_GRAPHQL_DISALLOW_INCONSISTENT_METADATA=true \
    HASURA_GRAPHQL_ENABLE_TELEMETRY=false \
    HOME=/tmp

COPY metadata /hasura-metadata

# nobody, the engine does not need root
USER 65534
