import pytest
import app as application


@pytest.fixture
def client(tmp_path):
    test_db = tmp_path / "test_print_queue.db"
    application.DB_NAME = str(test_db)
    application.app.config["TESTING"] = True
    application.init_db()

    with application.app.test_client() as client:
        yield client


def test_health_check(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.get_json()["status"] == "ok"


def test_submit_print_job_and_api(client):
    res = client.post(
        "/submit",
        data={"doc_name": "Report.pdf", "student_name": "Soham", "pages": "5"},
        follow_redirects=True,
    )
    assert res.status_code == 200

    api_res = client.get("/api/jobs")
    data = api_res.get_json()
    assert len(data) == 1
    assert data[0]["doc_name"] == "Report.pdf"
    assert data[0]["status"] == "Queued"


def test_submit_validation_rejection(client):
    res = client.post(
        "/submit",
        data={"doc_name": "Lab.pdf", "student_name": "Soham", "pages": "-2"},
    )
    assert res.status_code == 400


def test_empty_student_name_rejected(client):
    res = client.post(
        "/submit",
        data={"doc_name": "Thesis.pdf", "student_name": "", "pages": "5"},
    )
    assert res.status_code == 400


def test_zero_pages_rejected(client):
    res = client.post(
        "/submit",
        data={"doc_name": "Project.pdf", "student_name": "Soham", "pages": "0"},
    )
    assert res.status_code == 400


def test_mark_job_ready(client):
    client.post(
        "/submit",
        data={"doc_name": "Notes.pdf", "student_name": "Soham", "pages": "10"},
    )
    res = client.post("/ready/1", follow_redirects=True)
    assert res.status_code == 200

    api_res = client.get("/api/jobs")
    assert api_res.get_json()[0]["status"] == "Ready for Pickup"


def test_clear_ready_jobs(client):
    client.post(
        "/submit",
        data={"doc_name": "ClearTest.pdf", "student_name": "Soham", "pages": "2"},
    )
    client.post("/ready/1", follow_redirects=True)
    res = client.post("/clear-ready", follow_redirects=True)
    assert res.status_code == 200

    api_res = client.get("/api/jobs")
    assert len(api_res.get_json()) == 0


def test_api_stats(client):
    client.post(
        "/submit",
        data={"doc_name": "StatsDoc.pdf", "student_name": "Soham", "pages": "12"},
    )
    res = client.get("/api/stats")
    assert res.status_code == 200
    data = res.get_json()
    assert data["total_jobs"] == 1
    assert data["total_pages"] == 12