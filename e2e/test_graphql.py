import requests


def test_hasura_metadata_is_consistent(service):
    # strict: 500 when the metadata tracks a table or column the indexer does not have
    r = requests.get(service("hasura", 8080) + "/healthz?strict=true", timeout=10)
    assert r.status_code == 200


# Hasura runs only the operations of the contract for anonymous clients
# (hasura/metadata/query_collections.yaml), so the test sends LatestBlocks of
# web-api.graphql exactly as the allow-list has it.
LATEST_BLOCKS = """
query LatestBlocks($limit: Int = 10) {
  blocks(where: {canonical: {_eq: true}}, order_by: {height: desc}, limit: $limit) {
    ...BlockRow
  }
}

fragment BlockRow on blocks {
  hash
  height
  time
  miner
  transfer_count
  registration_count
  proof_count
  fee_total
}
"""


def test_anonymous_reads_the_blocks_view(service):
    # Without a token: the role anonymous over the api views of pouw-indexer
    r = requests.post(service("hasura", 8080) + "/v1/graphql",
                      json={"query": LATEST_BLOCKS, "variables": {"limit": 1}},
                      timeout=10)
    assert r.status_code == 200
    body = r.json()
    assert "errors" not in body, body
    assert isinstance(body["data"]["blocks"], list)


def test_explorer_page(service):
    r = requests.get(service("dashboard", 8080) + "/", timeout=10)
    assert r.status_code == 200


def test_anonymous_cannot_run_other_queries(service):
    # A query outside the contract is rejected, even if it only reads
    r = requests.post(service("hasura", 8080) + "/v1/graphql",
                      json={"query": "{ blocks(limit: 1) { hash } }"},
                      timeout=10)
    assert r.status_code == 200
    assert "not allowed" in r.text, r.text


def test_manage_info(service):
    # what runs here: version, commit, branch and build time of the image
    r = requests.get(service("dashboard", 8080) + "/manage/info", timeout=10)
    assert r.status_code == 200
    info = r.json()
    assert info["service"] == "pouw-dashboard"
    assert {"version", "commit", "branch", "build_time"} <= info.keys()
