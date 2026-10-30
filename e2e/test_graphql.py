import requests


def test_hasura_metadata_is_consistent(service):
    # strict: 500 when the metadata tracks a table or column the indexer does not have
    r = requests.get(service("hasura", 8080) + "/healthz?strict=true", timeout=10)
    assert r.status_code == 200


def test_graphql_answers(service):
    r = requests.post(service("hasura", 8080) + "/v1/graphql",
                      json={"query": "{ __typename }"}, timeout=10)
    assert r.status_code == 200
    assert "data" in r.json() or "errors" in r.json()


def test_explorer_page(service):
    r = requests.get(service("dashboard", 8080) + "/", timeout=10)
    assert r.status_code == 200
