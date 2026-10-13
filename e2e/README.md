# e2e

End-to-end tests against a running PoUW network. Unit tests stay in `tests/`
and run in GitHub Actions (`ci-ok`). These run in Jenkins: every evening on
`main` before the deploy to staging, and on every PR in `pouw-deploy`.

Add a `test_*.py` file here, nothing else is needed:

```python
import requests


def test_health():
    r = requests.get("http://dashboard:8000/health", timeout=10)
    assert r.status_code == 200
```

If you want use different language instead Python, communicate with @Faustynn, and after you need to provide a `run.sh` script.

- Services are reached by their name in `compose.yml` of `pouw-deploy`, there
  are no ports on the host.
- Extra libraries (e.g. `zeep` for SOAP) go into `requirements.txt`.
- Tests that are not pytest: replace the body of `run.sh` and keep its
  contract (argument, `JUNIT_DIR`, exit code).

Run locally from `pouw-deploy`: images are built from `main`, the tests are
taken from your working copies next to it.

```bash
make images test IMAGE_TAG=local E2E_SRC=..
make test-down
```

More in the docs: CI/CD, section E2E tests of services.
