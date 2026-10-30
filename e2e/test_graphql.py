import requests


def test_hasura_metadata_is_consistent(service):
    # strict: 500 when the metadata tracks a table or column the indexer does not have
    r = requests.get(service("hasura", 8080) + "/healthz?strict=true", timeout=10)
    assert r.status_code == 200


def test_anonymous_reads_the_blocks_view(service):
    # Without a token: the role anonymous over the api views of pouw-indexer
    r = requests.post(service("hasura", 8080) + "/v1/graphql",
                      json={"query": "{ blocks(limit: 1, order_by: {height: desc}) { hash height } }"},
                      timeout=10)
    assert r.status_code == 200
    body = r.json()
    assert "errors" not in body, body
    assert isinstance(body["data"]["blocks"], list)


def test_explorer_page(service):
    r = requests.get(service("dashboard", 8080) + "/", timeout=10)
    assert r.status_code == 200
