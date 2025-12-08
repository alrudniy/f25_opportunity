import pytest
from opportunity_company_info.app import app

@pytest.fixture
def client():
    """Configures the app for testing, disables error catching."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_about_page(client):
    """Test that the /company/about page loads successfully and contains expected content."""
    response = client.get('/company/about')
    assert response.status_code == 200
    assert b"About Opportunity Company" in response.data
    assert b"Our Mission" in response.data

def test_home_page(client):
    """Test that the /company/home page loads successfully and contains expected content."""
    response = client.get('/company/home')
    assert response.status_code == 200
    assert b"Unlock Your Potential with Opportunity Company" in response.data
    assert b"What We Offer" in response.data
