# pouw-dashboard
Web dashboard and block explorer

## Structure

| Directory | What | Image |
|---|---|---|
| `web/` | Explorer UI (React, Vite). `npm ci`, `npm run lint`, `npm test`, `npm run build` | `ghcr.io/pouw-zk/pouw-dashboard` (nginx on port 8080) |
| `hasura/` | Hasura project: `metadata/` (tracked tables, relationships, permissions), `seeds/default/*.sql` (fake data) | `ghcr.io/pouw-zk/pouw-dashboard-hasura` |
| `e2e/` | Tests against the running network, called from pouw-deploy | - |

The database schema is owned by [pouw-indexer](https://github.com/PoUW-ZK/pouw-indexer)
(Alembic), Hasura only tracks it. That is why `hasura/` has no `migrations/`.

The Hasura image applies `metadata/` on start and does not start when the
metadata references a table or column that does not exist. CI checks the same:
the `hasura` job creates the schema with `alembic upgrade head` from pouw-indexer
(until it has migrations, `hasura/seeds/default/*.sql` may create the tables),
starts the image and checks the metadata consistency.

Working with the metadata locally (Hasura console, export after changes):

```bash
export HASURA_GRAPHQL_ADMIN_SECRET=<secret>
hasura console --project hasura          # endpoint from hasura/config.yaml
hasura metadata export --project hasura  # commit the changes in hasura/metadata
```
