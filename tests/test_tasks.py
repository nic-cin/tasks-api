import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.database import get_session
from app.main import app


@pytest.fixture(name="client")
def client_fixture():
    """Cria um banco em memoria e faz a API usar ele em vez do tasks.db."""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)

    def get_session_override():
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_session] = get_session_override
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_root(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_create_task(client):
    resp = client.post("/tasks/", json={"title": "estudar pytest", "description": "etapa 4"})
    assert resp.status_code == 201
    body = resp.json()
    assert body["id"] == 1
    assert body["title"] == "estudar pytest"
    assert body["done"] is False


def test_create_task_empty_title_is_rejected(client):
    resp = client.post("/tasks/", json={"title": ""})
    assert resp.status_code == 422


def test_list_tasks(client):
    client.post("/tasks/", json={"title": "a"})
    client.post("/tasks/", json={"title": "b"})
    resp = client.get("/tasks/")
    assert resp.status_code == 200
    assert len(resp.json()) == 2


def test_get_task_not_found(client):
    resp = client.get("/tasks/99")
    assert resp.status_code == 404


def test_update_task(client):
    task_id = client.post("/tasks/", json={"title": "pendente"}).json()["id"]
    resp = client.patch(f"/tasks/{task_id}", json={"done": True})
    assert resp.status_code == 200
    assert resp.json()["done"] is True
    assert resp.json()["title"] == "pendente"  # nao mudou o que nao foi enviado


def test_delete_task(client):
    task_id = client.post("/tasks/", json={"title": "apagar"}).json()["id"]
    resp = client.delete(f"/tasks/{task_id}")
    assert resp.status_code == 204
    assert client.get(f"/tasks/{task_id}").status_code == 404


def test_filter_done_tasks(client):
    a = client.post("/tasks/", json={"title": "feita"}).json()["id"]
    client.post("/tasks/", json={"title": "pendente"})
    client.patch(f"/tasks/{a}", json={"done": True})

    done = client.get("/tasks/?done=true").json()
    pending = client.get("/tasks/?done=false").json()
    assert [t["title"] for t in done] == ["feita"]
    assert [t["title"] for t in pending] == ["pendente"]


def test_filter_invalid_value(client):
    assert client.get("/tasks/?done=talvez").status_code == 422