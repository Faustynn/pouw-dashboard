# e2e tests need a running network, run.sh sets E2E_PROJECT. Without it, e.g.
# plain `pytest` for unit tests in ci-ok, this directory is skipped.
import os

if not os.environ.get("E2E_PROJECT"):
    collect_ignore_glob = ["*"]
