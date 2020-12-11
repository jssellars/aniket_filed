def test_healthcheck(client):
    assert client.get("/api/v1/healthcheck").status_code == 200


def test_version(client):
    assert client.get("/api/v1/version").status_code == 200
