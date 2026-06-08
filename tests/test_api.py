import pytest


@pytest.mark.api
class TestApi:

    def test_get_all_posts(self, api_client):
        response = api_client.get("/posts")
        assert response.status_code == 200
        assert len(response.json()) == 100

    def test_get_single_post(self, api_client):
        response = api_client.get("/posts/1")
        assert response.status_code == 200
        assert response.json()["id"] == 1

    def test_create_post(self, api_client):
        payload = {"title": "foo", "body": "bar", "userId": 1}
        response = api_client.post("/posts", payload)
        assert response.status_code == 201
        assert response.json()["title"] == "foo"

    def test_update_post(self, api_client):
        payload = {"id": 1, "title": "updated title", "body": "updated body", "userId": 1}
        response = api_client.put("/posts/1", payload)
        assert response.status_code == 200
        assert response.json()["title"] == "updated title"

    def test_delete_post(self, api_client):
        response = api_client.delete("/posts/1")
        assert response.status_code == 200
