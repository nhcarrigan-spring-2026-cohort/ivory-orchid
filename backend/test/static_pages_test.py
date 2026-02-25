import pytest

from . import app

@pytest.fixture
def client():
	app.testing = True
	return app.test_client()

def test_main_page(client):
	response = client.get("/")
	assert response.status_code == 200
	assert b"Every pet deserves a home." in response.data
	
def test_non_existent_page(client):
	response = client.get("/" + "asfdasxfbg765gdh7udusyzh5er7u7iyhzrfh76zdusyh76tgf467sdedt/s7drhyf76hsztred/s78drye")
	assert response.status_code == 404
	assert b"Page Not Found" in response.data or b"Page not found" in response.data