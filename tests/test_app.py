import os
from fastapi.testclient import TestClient

# Ensure default admin token is predictable for tests
os.environ.setdefault("ADMIN_TOKEN", "change-me-in-production")

from main import app  # noqa: E402

client = TestClient(app)


def test_health_ok():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json().get("status") == "ok"


def test_projects_list_page():
    r = client.get("/projects")
    assert r.status_code == 200
    # Contains heading
    assert "Projects" in r.text


def test_add_project_admin_guarded():
    # Without auth should fail
    r = client.post("/projects", data={"name": "T1", "description": "d"})
    assert r.status_code in (401, 403)

    # With correct token should succeed (returns an HTML fragment)
    r = client.post(
        "/projects",
        headers={"Authorization": "Bearer change-me-in-production"},
        data={
            "name": "Test Project",
            "description": "A short description",
            "url": "https://example.com",
        },
    )
    assert r.status_code == 200
    assert "Test Project" in r.text

